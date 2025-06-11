terraform {
  required_version = ">= 0.12"
  required_providers {
    azapi = {
      source  = "Azure/azapi"
      version = "~> 2.3"
    }

    azurerm = {
      source  = "azurerm"
      version = "~> 4.17.0"
    }

    random = {
      source  = "random"
      version = "~> 3.7"
    }
  }
}
