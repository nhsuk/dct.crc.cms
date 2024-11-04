provider "azurerm" {
  resource_provider_registrations = "none"
  features {}
}

provider "azurerm" {
  alias                           = "database"
  resource_provider_registrations = "none"
  features {}
  subscription_id = var.environment == "integration" ? "07748954-52d6-46ce-95e6-2701bfc715b4" : null
}

provider "azapi" {
}
