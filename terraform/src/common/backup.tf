module "backup" {
  source                     = "git::https://github.com/NHSDigital/az-backup.git//infrastructure?ref=df197d74612a6a3b7214b126aaa0384c0b66b9eb" # commit hash of pr-68 fix role assignments
  resource_group_name        = "dct-${local.app}-vault-rg-${var.environment}-${var.location}"
  resource_group_location    = var.long_location
  backup_vault_name          = "dct-${local.app}-bv-${var.environment}-${var.location}"
  backup_vault_immutability  = "Unlocked"
  log_analytics_workspace_id = data.azurerm_log_analytics_workspace.shared_log_analytics_workspace[0].id

  use_extended_retention = true

  tags = data.azurerm_resource_group.rg.tags

  blob_storage_backups = {
    backup_crc = {
      backup_name                = "dct-${local.app}-bkp-blob-${var.env}"
      retention_period           = "P1M"
      backup_intervals           = ["R/2024-01-01T00:00:00+00:00/P1D"]
      storage_account_id         = azurerm_storage_account.crc_cms_storage_account.id
      storage_account_containers = [azurerm_storage_container.campaigns_crc.name]
    }
  }
}