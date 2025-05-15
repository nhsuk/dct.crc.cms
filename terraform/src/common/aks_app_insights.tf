resource "azurerm_log_analytics_workspace" "log_analytics_workspace" {
  count = var.environment == "development" ? 0 : 1

  name                = local.log_analytics_workspace_name
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  retention_in_days   = 30
}

resource "azurerm_application_insights" "aks_app_insights" {
  name                = local.aks_app_insights_name
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  workspace_id        = var.environment == "development" ? data.azurerm_log_analytics_workspace.shared_log_analytics_workspace[0].id : azurerm_log_analytics_workspace.log_analytics_workspace[0].id
  application_type    = "web"
}
