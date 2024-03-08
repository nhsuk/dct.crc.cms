data "azurerm_managed_api" "kv" {
  name     = "keyvault"
  location = local.location_long
}
