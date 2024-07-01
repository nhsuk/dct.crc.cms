module "nhsuk" {  
  count       = var.environment != "integration" ? 1 : 0
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
