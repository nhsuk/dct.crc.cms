
resource "azurerm_load_test" "lt" {
  location            = data.azurerm_resource_group.rg.location
  name                = var.load_testing_resource
  resource_group_name = data.azurerm_resource_group.rg.name
}
