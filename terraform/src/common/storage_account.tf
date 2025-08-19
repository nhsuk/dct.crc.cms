locals {
  locs = {
    "devuks" : ["campaignscrcv3strgdevuks"]
    "intuks" : ["campaignscrcv3strgintuks"]
    "staguks" : ["campaignscrcv3staguks"]
    "produks" : ["campaignscrcv3produks"]
    "produkw" : []
  }
}

import {
  for_each = toset(local.locs["${var.env}${var.location}"])
  to       = azurerm_storage_account.crc_cms[each.key]
  id       = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Storage/storageAccounts/${each.value}"
}


# # Create a storage account
resource "azurerm_storage_account" "crc_cms" {
  for_each                 = toset(local.locs["${var.env}${var.location}"])
  name                     = each.value
  resource_group_name      = var.resource_group
  location                 = var.long_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}