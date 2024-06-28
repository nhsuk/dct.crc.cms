module "nhsuk" {  
  count       = var.environment == "development" ? 1 : 0  
  source      = "./modules/activeconnectionsalert"  
  environment = var.environment  
  location    = var.location  
}

module "nhsuk-integration" {  
  count       = var.environment == "integration" ? 1 : 0  
  source      = "./modules/activeconnectionsalert"  
  environment = var.environment  
  location    = var.location  
  providers = {  
    azurerm = azurerm.nhsuk-integration  
  }  
}

module "nhsuk-staging" {  
  count       = var.environment == "staging" ? 1 : 0  
  source      = "./modules/activeconnectionsalert"  
  environment = var.environment  
  location    = var.location  
  providers = {  
    azurerm = azurerm.nhsuk-staging  
  }  
}

module "nhsuk-production" {  
  count       = var.environment == "production" ? 1 : 0  
  source      = "./modules/activeconnectionsalert"  
  environment = var.environment  
  location    = var.location  
  providers = {  
    azurerm = azurerm.nhsuk-production  
  }  
}
