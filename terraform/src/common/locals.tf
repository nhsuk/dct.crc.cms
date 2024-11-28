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

  scheduler_logic_app_name         = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduler-la-")
  search_reindex_logic_app_name    = replace(data.azurerm_resource_group.rg.name, "-rg-", "-search-reindex-la-")
  key_vault_name                   = replace(data.azurerm_resource_group.rg.name, "-rg-", "-kv-")
  postgres_flex_name               = replace(data.azurerm_resource_group.rg.name, "-rg-", "-psql-")
  activeconnections_logic_app_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-la-")
  activeconnections_logic_app_id   = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Logic/workflows/${local.activeconnections_logic_app_name}"

  secret_names = [
    "alertingWebhook",
    "pubToken",
    "pubEndpoint",
    "searchIndexEndpoint"
  ]

  deploy_database = var.location == "uks" # Only deploy database module for primary regions (replica will be deployed to dr)
}
