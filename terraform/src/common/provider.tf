provider "azurerm" {  
  skip_provider_registration = true  
  features {}  
}

provider "azurerm" {  
  alias = "nhsuk-integration"  
  skip_provider_registration = true  
  features {}  
  subscription_id = "07748954-52d6-46ce-95e6-2701bfc715b4"  # nhsuk-development 
}

provider "azapi" {  
}
