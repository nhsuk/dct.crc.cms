data "azurerm_client_config" "current" {}

data "azurerm_log_analytics_workspace" "shared_log_analytics_workspace" {
  provider = azurerm.law

  name                = local.law_name
  resource_group_name = local.law_resource_group_name
}
