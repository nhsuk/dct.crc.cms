resource "azurerm_storage_account" "crc_cms_storage_account" {
  name                     = var.env == "prod" ? "campaignscrcv3produks" : (var.env == "stag" ? "campaignscrcv3staguks" :"campaignsstrgintuks")
  resource_group_name      = var.resource_group
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "GRS"
  min_tls_version          = "TLS1_2"
}

#trivy:ignore:avd-azu-0007 Storage container public access should be on because it serves the images for the website
resource "azurerm_storage_container" "campaigns_crc" {
  name                  = var.env == "prod" ? "campaign-resource-centre-v3-production" : (var.env == "stag" ? "campaign-resource-centre-v3-staging" :(var.env == "int" ? "campaign-resouce-centre-v3-integration" :"campaign-resouce-centre-v3-review"))
  storage_account_id    = azurerm_storage_account.crc_cms_storage_account.id
  container_access_type = "blob"
}