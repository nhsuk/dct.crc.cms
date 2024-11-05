#!/bin/bash

##
## Script to validate a migration from a postgres single server to postgres flexible server
##

set -e

# Check environment variables are set
required_env_vars=("ENVIRONMENT" "FLEX_SERVER_ADMIN_PASSWORD" "SINGLE_SERVER_ADMIN_PASSWORD" "DATABASE")
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

# prod has a different admin username
if [ "$ENVIRONMENT" == "prod" ]; then
  SINGLE_SERVER_ADMIN_USERNAME="cmsadmin"
else
  SINGLE_SERVER_ADMIN_USERNAME="betterhealth"
fi

echo "Cleaning up any containers..."
docker container rm --force new-validation old-validation

echo "Running script on new server..."

docker run \
  --env PGPASSWORD=$FLEX_SERVER_ADMIN_PASSWORD \
  --name new-validation \
  --volume ./validation.sql:/validation.sql \
  postgres psql \
  --username=cmsadmin \
  --host=dct-crccms-psql-$ENVIRONMENT-uks.postgres.database.azure.com \
  --file /validation.sql \
  $DATABASE

docker logs new-validation >new-validation.log 2>&1

echo "Running script on old server..."

docker run \
  --env PGPASSWORD=$SINGLE_SERVER_ADMIN_PASSWORD \
  --name old-validation \
  --volume ./validation.sql:/validation.sql \
  postgres psql \
  --username=$SINGLE_SERVER_ADMIN_USERNAME@campaigns-cms-psql-$SOURCE_ENVIRONMENT-uks.postgres.database.azure.com \
  --host=campaigns-cms-psql-$SOURCE_ENVIRONMENT-uks.postgres.database.azure.com \
  --file /validation.sql \
  $DATABASE

docker logs old-validation >old-validation.log 2>&1

echo "Running diff..."
set +e
diff old-validation.log new-validation.log

VALIDATION_FAILED=$?

if [ $VALIDATION_FAILED -ne 0 ]; then
  echo "##vso[task.logissue type=warning;]Data validation has failed"
  echo "##vso[task.complete result=SucceededWithIssues;]"
fi
