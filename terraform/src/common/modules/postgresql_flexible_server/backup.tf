module "backup" {
  source                     = "git::https://github.com/NHSDigital/az-backup.git//infrastructure?ref=df197d74612a6a3b7214b126aaa0384c0b66b9eb" # commit hash of pr-68 fix role assignments
  resource_group_name        = "dct-${local.app}-vault-rg-${var.environment}-${var.location}"
  resource_group_location    = var.long_location
  backup_vault_name          = "dct-${local.app}-bv-${var.environment}-${var.location}"
  backup_vault_immutability  = "Unlocked"
  log_analytics_workspace_id = var.log_analytics_workspace_id

  use_extended_retention = true

  tags = data.azurerm_resource_group.default.tags

  postgresql_flexible_server_backups = {
    backup1 = {
      backup_name              = "dct-${local.app}-bkp-psql-${var.environment}"
      retention_period         = "P1M"
      backup_intervals         = ["R/2024-01-01T00:00:00+00:00/P1D"]
      server_id                = azurerm_postgresql_flexible_server.database.id
      server_resource_group_id = data.azurerm_resource_group.default.id
    }
  }
}