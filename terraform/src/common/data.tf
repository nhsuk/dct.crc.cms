/**
 * The resource group where all resources will be contained.
 * This terraform project doesn't create the resource group, the resource group
 * must already exist.
 */

data "azurerm_resource_group" "rg" {
  name = var.resource_group
}

/**
 * The database for this resource group (either primary in uksouth or replica in ukwest)
 */
data "azurerm_postgresql_flexible_server" "flex" {
  name                = local.postgres_flex_name
  resource_group_name = data.azurerm_resource_group.rg.name
}
