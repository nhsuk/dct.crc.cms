locals {
  common_tags = {
    "cost code"       = "P0406/02"
    "created by"      = "Azure Pipeline"
    "created date"    = "07/03/2024"
    "environment"     = var.environment
    "product owner"   = "Jeni Riordan"
    "requested by"    = "Evan Harris"
    "service-product" = "Campaigns CRC CMS"
    "team"            = "Digital Campaigns"
  }

  location_long = split("-", var.resource_group)[4] == "uks" ? "uksouth" : "ukwest"
  # subscription_id = split("/", var.resource_group)[2]
  # api_connection_id = "/subscriptions/${local.subscription_id}/providers/Microsoft.Web/locations/${local.location_long}/managedApis/keyvault"
}
