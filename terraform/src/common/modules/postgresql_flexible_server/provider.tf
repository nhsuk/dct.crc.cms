provider "azurerm" {
  features {}
  alias           = "law"
  subscription_id = var.environment == "prod" ? "0fc4b46b-edd5-4bfe-9ec6-52657a130d1b" : "bec2490a-01f4-4581-af1a-bd14223a71e6"
}