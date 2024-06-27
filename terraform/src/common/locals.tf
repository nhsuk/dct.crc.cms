locals {
  common_tags = {
    "cost code"       = "P0406/02"
    "created by"      = "Azure Pipeline"
    "created date"    = "07/03/2024"
    "environment"     = var.environment
    "product owner"   = "Jeni Riordan"
    "requested by"    = "Evan Harris"
    "service-product" = "Campaigns CRC CMS"
    "team"            = "Digital Campaigns"
  }

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

  scheduler_logic_app_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduler-la-")
  key_vault_name           = replace(data.azurerm_resource_group.rg.name, "-rg-", "-kv-")
  activeconnections_logic_app_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-la-")  
  activeconnections_logic_app_id = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Logic/workflows/${local.activeconnections_logic_app_name}"
  postgresql_server_resource_id = data.azurerm_postgresql_server.postgres_server.id
  postgresql_server_url = "https://portal.azure.com/#@nhschoices.net/resource${local.postgresql_server_resource_id}/overview"

  secret_names = [
    "alertingWebhook",
    "pubToken",
    "pubEndpoint"
  ]
}
