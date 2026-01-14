provider "azurerm" {
  resource_provider_registrations = "none"
  features {}
}

provider "azapi" {
}

provider "azurerm" {
  features {}
  alias           = "law"
  subscription_id = var.env == "prod" ? "0fc4b46b-edd5-4bfe-9ec6-52657a130d1b" : "bec2490a-01f4-4581-af1a-bd14223a71e6"
  resource_provider_registrations = "none"
}

provider "azurerm" {
  features {}
  alias           = "hub"
  subscription_id = "d535b130-e970-4713-b547-0ba3cd149539"
  resource_provider_registrations = "none"
}

provider "azurerm" {
  features {}
  alias           = "config"
  subscription_id = var.env == "prod" ? "ed6103a2-2642-470e-b1fa-77bf35b7b3fc" : "2aed4d1b-245d-4bd8-99c5-b21e53c84b72" # dct-config-prod or API dct-config-int
  resource_provider_registrations = "none"
}
