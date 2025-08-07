import {
  to = azurerm_storage_account.crc_cms_storage_account
  id = "/subscriptions/${var.subscription_id}/resourceGroups/${var.resource_group}/providers/Microsoft.Storage/storageAccounts/${var.storage_account_name}"
}

resource "azurerm_storage_account" "crc_cms_storage_account" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group
  location                 = var.long_location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  min_tls_version          = "TLS1_2"
}

#trivy:ignore:avd-azu-0007 Storage container public access should be on because it serves the images for the website
resource "azurerm_storage_container" "campaigns_crc" {
  name                  = var.storage_account_container
  storage_account_id    = azurerm_storage_account.crc_cms_storage_account.id
  container_access_type = "blob"
}