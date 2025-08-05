module "database" {
  count = local.deploy_database ? 1 : 0

  source                     = "./modules/postgresql_flexible_server"
  name                       = local.postgres_flex_name
  resource_group             = data.azurerm_resource_group.rg
  environment                = var.environment
  key_vault                  = azurerm_key_vault.kv
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace

  providers = {
    azurerm.law = azurerm.law
  }
}
