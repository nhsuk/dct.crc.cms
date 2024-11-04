#!/bin/bash

##
## Script to migrate a postgres single server to postgres flexible server
##

set -e

# Check environment variables are set
required_env_vars=("MIGRATION_ID" "SUBSCRIPTION" "ENVIRONMENT" "SINGLE_SERVER_ADMIN_PASSWORD" "FLEX_SERVER_ADMIN_PASSWORD" "DATABASE" "CRC_PASSWORD" "MIGRATION_OPTION")
for var in "${required_env_vars[@]}"; do
  if [[ -z "${!var}" ]]; then
    echo "'$var' is not set"
    exit 1
  fi
done

# int is currently using the dev database server so source it from there
if [[ "$ENVIRONMENT" == "int" ]]; then
  SOURCE_ENVIRONMENT="dev"
else
  SOURCE_ENVIRONMENT=$ENVIRONMENT
fi

# stag is currently using a different naming convention for resource group
if [[ "$ENVIRONMENT" == "stag" ]]; then
  SOURCE_RG="dct-cms-postgres-rg-stag-uksouth"
else
  SOURCE_RG="nhsuk-dct-rg-$SOURCE_ENVIRONMENT-uks"
fi

echo "Creating properties from template and env..."

jq \
  --null-input \
  --arg sourceDbServerResourceId /subscriptions/$SUBSCRIPTION/resourceGroups/$SOURCE_RG/providers/Microsoft.DBforPostgreSQL/servers/campaigns-cms-psql-$SOURCE_ENVIRONMENT-uks \
  --arg singleServerAdminPassword $SINGLE_SERVER_ADMIN_PASSWORD \
  --arg postgresqlAdminPassword $FLEX_SERVER_ADMIN_PASSWORD \
  --arg database $DATABASE \
  --from-file migration-properties.jq \
  >properties.json

echo "Starting validation and migration..."

az postgres flexible-server migration create \
  --resource-group dct-crccms-rg-$ENVIRONMENT-uks \
  --name dct-crccms-psql-$ENVIRONMENT-uks \
  --migration-name dct-crccms-psql-migration-$MIGRATION_ID-$ENVIRONMENT-uks \
  --migration-mode offline \
  --migration-option $MIGRATION_OPTION \
  --properties "properties.json"

while
  sleep 5
  echo "Checking migration status..."
  status=$(az postgres flexible-server migration show \
    --resource-group dct-crccms-rg-$ENVIRONMENT-uks \
    --name dct-crccms-psql-$ENVIRONMENT-uks \
    --migration-name dct-crccms-psql-migration-$MIGRATION_ID-$ENVIRONMENT-uks \
    --query "[currentStatus.state, currentStatus.currentSubStateDetails.currentSubState]" \
    --output tsv)
  printf "Status: $status\n\n"
  [[ "$status" =~ ^InProgress.* || "$status" =~ ^CleaningUp.* ]]
do true; done

if [[ ! "$status" =~ ^Succeeded ]]; then
  exit 2
fi

echo "Setting up crc user and changinging ownership of database objects..."

docker run --env PGPASSWORD=$FLEX_SERVER_ADMIN_PASSWORD postgres psql \
  --username=cmsadmin \
  --host=dct-crccms-psql-$ENVIRONMENT-uks.postgres.database.azure.com \
  --command "
    DO \$\$
    BEGIN
      IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '$DATABASE') THEN
        CREATE USER $DATABASE WITH ENCRYPTED PASSWORD '$CRC_PASSWORD';
      END IF;
    END \$\$;
    GRANT $DATABASE TO cmsadmin;
    ALTER DATABASE $DATABASE OWNER TO $DATABASE;
    REASSIGN OWNED BY cmsadmin TO $DATABASE;
  " \
  $DATABASE
