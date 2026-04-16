resource "azurerm_storage_account" "crc_cms" {
  #checkov:skip=CKV_AZURE_33 No logging currently enabled https://ukhsa.atlassian.net/browse/BH-2261
  #checkov:skip=CKV_AZURE_59 Storage account is public because it serves assets for the website
  #checkov:skip=CKV_AZURE_190 Storage account is public because it serves assets for the website
  #checkov:skip=CKV2_AZURE_1 Customer managed key not required
  #checkov:skip=CKV2_AZURE_8 Activity logs are not exported to storage account
  #checkov:skip=CKV2_AZURE_21 No logging currently enabled https://ukhsa.atlassian.net/browse/BH-2261
  #checkov:skip=CKV2_AZURE_33 Storage account is public because it serves assets for the website
  #checkov:skip=CKV2_AZURE_40 Storage account shared access key will be removed (https://ukhsa.atlassian.net/browse/CV-1425)
  #checkov:skip=CKV2_AZURE_41 Storage account SAS tokens are not used
  #checkov:skip=CKV2_AZURE_47 Storage account is public because it serves assets for the website
  for_each = local.storage_account

  name                     = each.value
  resource_group_name      = var.resource_group
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  min_tls_version          = "TLS1_2"

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

resource "azurerm_storage_container" "crc_cms" {
  #checkov:skip=CKV_AZURE_34 Storage container public access should be on because it serves the images for the website
  #checkov:skip=CKV2_AZURE_21 No logging currently enabled https://ukhsa.atlassian.net/browse/BH-2261
  #checkov:skip=CKV2_AZURE_8 Activity logs are not exported to storage account
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
  #checkov:skip=CKV2_AZURE_33 Access required from ADO hosted agents and Developers laptops
  #checkov:skip=CKV2_AZURE_1 Customer managed key not required
  count = var.env == "dev" ? 1 : 0

  name                     = "dctcrccmsbackups${var.env}${var.location}"
  resource_group_name      = var.resource_group
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"

  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false

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

resource "azurerm_storage_container" "crc_cms_backups" {
  #checkov:skip=CKV_AZURE_33 No logging currently enabled https://ukhsa.atlassian.net/browse/BH-2261
  #checkov:skip=CKV2_AZURE_21 No logging currently enabled https://ukhsa.atlassian.net/browse/BH-2261
  for_each = var.env == "dev" ? toset(["review", "integration", "staging"]) : toset([])

  name                  = each.value
  storage_account_id    = azurerm_storage_account.crc_cms_backups[0].id
  container_access_type = "private"
}

resource "azurerm_role_assignment" "backups_blob_contributor_pipeline_identity" {
  count = var.env == "dev" ? 1 : 0

  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = azurerm_storage_account.crc_cms_backups[0].id
  principal_type       = "ServicePrincipal"
}