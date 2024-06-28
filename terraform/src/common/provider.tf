provider "azurerm" {
  skip_provider_registration = true
  features {}
}

provider "azurerm" {
  alias = "nhsuk-integration"
  skip_provider_registration = true
  features {}
  subscription_id = "2cf44e0d-817d-4596-b471-0788f8a14ab2"
}

provider "azapi" {
}

# provider "azurerm" {
#   alias = "nhsuk-staging"
#   skip_provider_registration = true
#   features {}
#   subscription_id = "b0787d6a-56e3-4899-bc30-723f9d78899c"
# }

