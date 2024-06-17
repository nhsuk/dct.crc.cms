locals {
  common_tags = {
    "cost code"       = "P0406/02"
    "created by"      = "Azure Pipeline"
    "created date"    = "17/06/2024"
    "environment"     = var.environment
    "product owner"   = "Jeni Riordan"
    "requested by"    = "Evan Harris"
    "service-product" = "Campaigns Testing"
    "team"            = "Digital Campaigns"
  }
}
