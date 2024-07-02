module "activeconnectionsalert" {  
  count       = var.environment != "integration" ? 1 : 0
  source      = "./modules/activeconnectionsalert"  
  environment = var.environment  
  location    = var.location  
}

# This is required as the integration environment still uses the development postgresql server
module "activeconnectionsalert-integration" {  
  count       = var.environment == "integration" ? 1 : 0  
  source      = "./modules/activeconnectionsalert"  
  environment = var.environment  
  location    = var.location  
  providers = {  
    azurerm = azurerm.nhsuk-development
  }  
}
