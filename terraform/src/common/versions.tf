terraform {
  required_version = ">= 1.9"
  required_providers {
    azapi = {
      source  = "Azure/azapi"
      version = "~> 2.3"
    }

    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.38.1"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.7"
    }
  }
}
