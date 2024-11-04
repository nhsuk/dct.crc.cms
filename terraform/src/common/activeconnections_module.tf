module "activeconnectionsalert" {
  source      = "./modules/activeconnectionsalert"
  environment = var.environment
  location    = var.location
  providers = {
    azurerm = azurerm.database
  }
}
