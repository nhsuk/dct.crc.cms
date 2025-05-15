/**
 * The resource group where all resources will be contained.
 * This terraform project doesn't create the resource group, the resource group
 * must already exist.
 */

data "azurerm_resource_group" "rg" {
  name = var.resource_group
}

data "azurerm_log_analytics_workspace" "shared_log_analytics_workspace" {
  provider = azurerm.law

  name                = local.law_name
  resource_group_name = local.law_resource_group_name
}
