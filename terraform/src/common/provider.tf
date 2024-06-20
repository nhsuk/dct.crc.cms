provider "azurerm" {
  skip_provider_registration = true
  features {}
}

provider "azapi" {
}

provider "azuread" {
  tenant_id = "d9fec63b-47ed-4fa5-a265-1d3bb934a78b" # NHS.UK Azure AD tenant Id
}
