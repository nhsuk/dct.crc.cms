module "config" {
  source = "./modules/config"
  env    = var.env

  providers = {
    azurerm = azurerm.config
  }
}