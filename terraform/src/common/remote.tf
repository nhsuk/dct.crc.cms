terraform {
  backend "azurerm" {
    resource_group_name  = data.azurerm_resource_group.rg.name
    storage_account_name = var.tfstate_account_name
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    use_azuread_auth     = true
  }
}
