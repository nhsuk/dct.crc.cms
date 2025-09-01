import {
  for_each = local.storage_account
  to       = azurerm_storage_account.crc_cms[each.key]
  id       = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Storage/storageAccounts/${each.value}"
}

resource "azurerm_storage_account" "crc_cms" {
  for_each = local.storage_account

  name                     = each.value
  resource_group_name      = var.resource_group
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  blob_properties {
    last_access_time_enabled = true
    delete_retention_policy {
      days = 7
    }
    container_delete_retention_policy {
      days = 7
    }
  }
}

import {
  for_each = local.storage_container
  to       = azurerm_storage_container.crc_cms[each.key]
  id       = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Storage/storageAccounts/${each.value}/blobServices/default/containers/${each.key}"
}

#trivy:ignore:avd-azu-0007 storage container public access is enabled as it serves the assets for the website
resource "azurerm_storage_container" "crc_cms" {
  for_each = local.storage_container

  name                  = each.key
  storage_account_id    = azurerm_storage_account.crc_cms[each.value].id
  container_access_type = "blob"
}
