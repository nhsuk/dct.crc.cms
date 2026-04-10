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

resource "azurerm_role_assignment" "storage_blob_contributor_dev_identity" {
  count = var.env == "int" ? 1 : 0

  principal_id         = "84ef78f0-e0f9-4844-8d13-d1d494b7f42e" # dct-crccms-id-dev managed identity
  role_definition_name = "Storage Blob Data Contributor"
  scope                = data.azurerm_storage_container.dev[0].id
  principal_type       = "ServicePrincipal"

  # Requires Infra to remove lock on storage account before removing (i.e returning to default = false)
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "non_prod_storage_blob_contributor_pipeline_identity" {
  for_each = local.non_prod_storage_container_ids

  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = each.value
  principal_type       = "ServicePrincipal"
}

resource "azurerm_storage_account" "crc_cms_backups" {
  count = var.env == "dev" ? 1 : 0

  name                      = "dctcrccmsbackups${var.env}${var.location}"
  resource_group_name       = var.resource_group
  location                  = data.azurerm_resource_group.rg.location
  account_tier              = "Standard"
  account_replication_type  = "RAGRS"
  shared_access_key_enabled = false

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
  for_each = var.env == "dev" ? toset(["review", "integration", "staging", "production"]) : toset([])

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