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

  scheduler_logic_app_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduler-la-")
  key_vault_name           = replace(data.azurerm_resource_group.rg.name, "-rg-", "-kv-")
  activeconnections_logic_app_name = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-la-")
  activeconnections_logic_app_id = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Logic/workflows/${local.activeconnections_logic_app_name}"
  
  activeconnectionsalert_environment_map = {
    development  = module.activeconnectionsalert
    integration  = module.activeconnectionsalert-integration
    staging      = module.activeconnectionsalert
    production   = module.activeconnectionsalert
  }

  selected_environment = lookup(local.activeconnectionsalert_environment_map, var.environment)[0]

  postgresql_server_resource_id = local.selected_environment.postgresql_server_id
  postgresql_server_name        = local.selected_environment.postgresql_server_name
  postgresql_server_url         = "https://portal.azure.com/#@nhschoices.net/resource${local.postgresql_server_resource_id}/overview"

  secret_names = [  
    "alertingWebhook",
    "pubToken",
    "pubEndpoint"
  ]  
}
