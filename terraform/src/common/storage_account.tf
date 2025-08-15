locals {
    locs = [
        "devuks",
        "intuks",
        "staguks",
        "produks",
        "produkw"
    ]
}

# import doesn't allow count and doesn't currently have a create if don't exist so we need to cycle through using for_each and only import loc/env matches and it's not ukw which currently doesn't exist
import {
    for_each = local.locs == "${var.env}${var.location}" && local.locs != "produkw" ? [1]:[0]
    to = azurerm_storage_account.crc_cms
    id = "/subscriptions/${var.imported_storage_subscription_id}/resourceGroups/${var.imported_storage_resource_group}/providers/Microsoft.Storage/storageAccounts/${var.imported_storage_name}"
}


# # Create a storage account
resource "azurerm_storage_account" "crc_cms" {
  name                     = "campaignscrcv3strg${var.env}${var.location}"
  resource_group_name      = var.resource_group
  location                 = var.long_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}