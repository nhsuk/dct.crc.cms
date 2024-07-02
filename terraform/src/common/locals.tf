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
  
  environment_map = {
    development  = module.nhsuk
    integration  = module.nhsuk-integration
    staging      = module.nhsuk
    production   = module.nhsuk
  }

  selected_environment = lookup(local.environment_map, var.environment, null)

  postgresql_server_resource_id = local.selected_environment != null ? local.selected_environment[0].postgresql_server_id : null
  postgresql_server_name        = local.selected_environment != null ? local.selected_environment[0].postgresql_server_name : null
  postgresql_resource_group     = local.selected_environment != null ? local.selected_environment[0].postgresql_resource_group : null
  postgresql_server_url         = local.selected_environment != null ? "https://portal.azure.com/#@nhschoices.net/resource${local.postgresql_server_resource_id}/overview" : null

  secret_names = [  
    "alertingWebhook",
    "pubToken",
    "pubEndpoint"
  ]  
}
