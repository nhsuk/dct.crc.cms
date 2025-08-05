module "database" {
  count = local.deploy_database ? 1 : 0

  source         = "./modules/postgresql_flexible_server"
  name           = local.postgres_flex_name
  resource_group = data.azurerm_resource_group.rg
  environment    = var.environment
  key_vault      = azurerm_key_vault.kv
}

resource "azurerm_monitor_diagnostic_setting" "psql_logs" {
  name                       = "${local.prefix}-${local.app}-psql-logs-${var.env}-${local.region}"
  target_resource_id         = azurerm_postgresql_flexible_server.database.id
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace.id

  enabled_log {
    category_group = "audit"
  }

  enabled_metric {
    category = "AllMetrics"
  }
}