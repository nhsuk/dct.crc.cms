provider "azurerm" {
  resource_provider_registrations = "none"
  features {}
}

provider "azurerm" {
  alias                           = "nhsuk-development"
  resource_provider_registrations = "none"
  features {}
  subscription_id = "07748954-52d6-46ce-95e6-2701bfc715b4"
}

provider "azapi" {
}
