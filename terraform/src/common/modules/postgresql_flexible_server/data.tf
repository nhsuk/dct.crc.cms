# An existing resource group
data "azurerm_resource_group" "default" {
  name = var.resource_group.name
}


data "azurerm_client_config" "current" {}