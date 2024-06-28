provider "azurerm" {  
  skip_provider_registration = true  
  features {}  
}

provider "azurerm" {  
  alias = "nhsuk-integration"  
  skip_provider_registration = true  
  features {}  
  subscription_id = "07748954-52d6-46ce-95e6-2701bfc715b4"  # nhsuk-development 

provider "azurerm" {  
  alias = "nhsuk-staging"  
  skip_provider_registration = true  
  features {}  
  subscription_id = "b0787d6a-56e3-4899-bc30-723f9d78899c"   # nhsuk-staging 
}

provider "azurerm" {  
  alias = "nhsuk-production"  
  skip_provider_registration = true  
  features {}  
  subscription_id = "1e543650-5458-44ea-a3b1-35a6d0d92cc9"   # nhsuk (production)
}

provider "azapi" {  
}
