module "backup" {
  count = var.location == "uks" ? 1 : 0 # Only deploy backup vault to the primary region

  source                     = "git::https://github.com/NHSDigital/az-backup.git//infrastructure?ref=v2.0.3"
  resource_group_name        = local.backup_vault_resource_group_name
  resource_group_location    = data.azurerm_resource_group.rg.location
  backup_vault_name          = local.backup_vault_name
  backup_vault_immutability  = "Unlocked"
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace[0].id

  use_extended_retention = true

  tags = data.azurerm_resource_group.rg.tags

  postgresql_flexible_server_backups = {
    psql = {
      backup_name              = "dct-${local.app}-bkp-psql-${var.environment}"
      retention_period         = "P1M"
      backup_intervals         = ["R/2024-01-01T00:00:00+00:00/P1W"]
      server_id                = module.database[0].postgresql_flexible_server_id
      server_resource_group_id = data.azurerm_resource_group.rg.id
    }
  }
}
