terraform {
  required_version = ">= 1.9"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.17.0"
    }
  }
}

provider "azurerm" {
  resource_provider_registrations = "none"
  subscription_id                 = "f8a1a507-8a52-452c-84d4-ad20a8648f58" #dct-crccms-dev
  features {}
}
