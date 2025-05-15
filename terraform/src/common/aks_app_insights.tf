resource "azurerm_application_insights" "aks_app_insights" {
  name                = local.aks_app_insights_name
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  workspace_id        = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace.id
  application_type    = "web"
}
