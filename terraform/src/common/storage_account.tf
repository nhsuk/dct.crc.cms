locals {
  locs = {
    devuks : ["campaignscrcv3strgdevuks"]
    intuks : ["campaignsstrgintuks"]
    staguks : ["campaignsstrgstaguks"]
    produks : ["campaignscrcv3strgproduks"]
    produkw : []
  }
}

import {
  for_each = local.locs["${var.env}${var.location}"]
  to       = azurerm_storage_account.crc_cms
  id       = "${data.azurerm_resource_group.rg.id}/providers/Microsoft.Storage/storageAccounts/${each.value}"
}


# # Create a storage account
resource "azurerm_storage_account" "crc_cms" {
  for_each                 = local.locs["${var.env}${var.location}"]
  name                     = each.value
  resource_group_name      = var.resource_group
  location                 = var.long_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}