resource "azurerm_storage_account" "crc_cms" {
  for_each = local.storage_account

  name                     = each.value
  resource_group_name      = var.resource_group
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  blob_properties {
    change_feed_enabled           = true
    change_feed_retention_in_days = 7
    last_access_time_enabled      = true
    versioning_enabled            = true
    delete_retention_policy {
      days = 7
    }
    container_delete_retention_policy {
      days = 7
    }
  }
}

#trivy:ignore:avd-azu-0007 storage container public access is enabled as it serves the assets for the website
resource "azurerm_storage_container" "crc_cms" {
  for_each = local.storage_container

  name                  = each.key
  storage_account_id    = azurerm_storage_account.crc_cms[each.value].id
  container_access_type = "blob"
}

resource "azurerm_role_assignment" "storage_blob_contributor_pipeline_identity" {
  for_each = azurerm_storage_account.crc_cms

  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = each.value.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "storage_blob_contributor_apps_identity" {
  for_each = azurerm_storage_account.crc_cms

  principal_id         = data.azurerm_user_assigned_identity.apps.principal_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = each.value.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_storage_account" "crc_cms_backups" {
  count = var.env == "dev" ? 1 : 0

  name                     = "dctcrccmsbackups${var.env}${var.location}"
  resource_group_name      = var.resource_group
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  blob_properties {
    change_feed_enabled           = true
    change_feed_retention_in_days = 7
    last_access_time_enabled      = true
    versioning_enabled            = true
    delete_retention_policy {
      days = 7
    }
    container_delete_retention_policy {
      days = 7
    }
  }
}

#trivy:ignore:avd-azu-0007 storage container public access is enabled as it serves the assets for the website
resource "azurerm_storage_container" "crc_cms_backups" {
  for_each = var.env == "dev" ? ["review", "integration", "staging", "production"] : []

  name                  = each.value
  storage_account_id    = azurerm_storage_account.crc_cms_backups[0].id
  container_access_type = "container"
}

resource "azurerm_role_assignment" "backups_blob_contributor_pipeline_identity" {
  count = var.env == "dev" ? 1 : 0

  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = azurerm_storage_account.crc_cms_backups[0].id
  principal_type       = "ServicePrincipal"
}