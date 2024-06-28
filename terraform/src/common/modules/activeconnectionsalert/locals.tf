locals {
   postgresql_resource_groups = {
    development_uks  = "nhsuk-dct-rg-dev-uks"
    integration_uks  = "nhsuk-dct-rg-dev-uks"
    staging_uks = "dct-cms-postgres-rg-stag-uksouth"
    production_uks = "nhsuk-dct-rg-prod-uks"
    production_ukw = "nhsuk-dct-rg-prod-ukw"
  }

  postgresql_server_names = {
    development_uks  = "campaigns-cms-psql-dev-uks"
    integration_uks  = "campaigns-cms-psql-dev-uks"
    staging_uks = "campaigns-cms-psql-stag-uks"
    production_uks = "campaigns-cms-psql-prod-uks"
    production_ukw = "campaigns-cms-psql-prod-ukw"
  }

  env_location_key = "${var.environment}_${var.location}"
  postgresql_resource_group = local.postgresql_resource_groups[local.env_location_key]
  postgresql_server_name = local.postgresql_server_names[local.env_location_key]
}