locals {
  locs = {
    "devuks" : []
    "intuks" : ["campaignsstrgintuks"]
    "staguks" : ["campaignsstrgstaguks"]
    "stagukw" : []
    "produks" : ["campaignscrcv3produks"]
    "produkw" : []
  }
}

# # import storage account
import {
  for_each = toset(local.locs["${var.env}${var.location}"])
  to       = azurerm_storage_account.crc_cms[each.key]
  id       = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Storage/storageAccounts/${each.value}"
}

resource "azurerm_storage_account" "crc_cms" {
  for_each                 = toset(local.locs["${var.env}${var.location}"])
  name                     = each.value
  resource_group_name      = var.resource_group
  location                 = data.azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
}
