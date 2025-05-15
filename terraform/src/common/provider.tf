provider "azurerm" {
  resource_provider_registrations = "none"
  features {}
}

provider "azurerm" {
  alias                           = "database"
  resource_provider_registrations = "none"
  features {}
  # Integration database is in nhsuk-development subscription
  subscription_id = var.environment == "integration" ? "07748954-52d6-46ce-95e6-2701bfc715b4" : null
}

provider "azapi" {
}

provider "azurerm" {
  features {}
  alias           = "law"
  subscription_id = var.environment == "production" ? "0fc4b46b-edd5-4bfe-9ec6-52657a130d1b" : "bec2490a-01f4-4581-af1a-bd14223a71e6"
}
