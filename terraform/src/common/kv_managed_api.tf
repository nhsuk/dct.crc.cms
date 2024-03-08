data "azurerm_managed_api" "kv" {
  name     = "keyvault"
  location = data.azurerm_resource_group.rg.location
}
