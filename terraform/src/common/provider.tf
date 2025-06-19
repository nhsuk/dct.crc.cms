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
}

provider "azurerm" {
  features {}
  alias           = "hub"
  subscription_id = "d535b130-e970-4713-b547-0ba3cd149539"
}
