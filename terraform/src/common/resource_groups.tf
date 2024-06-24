/**
 * The resource group where all resources will be contained.
 * This terraform project doesn't create the resource group, the resource group
 * must already exist.
 */

data "azurerm_resource_group" "rg" {
  name = "${var.resource_group}"
}

data "azurerm_resource_group" "postgresql_rg" {
  name = "${var.postgresql_resource_group}"
}