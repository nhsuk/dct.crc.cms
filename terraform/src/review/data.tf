data "azurerm_resource_group" "wagtail" {
  name = "${local.org}-${local.app}-rg-${local.environment}-${local.region}"
}

data "azurerm_container_app_environment" "wagtail" {
  name                = "${local.org}-${local.app}-cae-${local.environment}-${local.region}"
  resource_group_name = data.azurerm_resource_group.wagtail.name
}

data "azurerm_user_assigned_identity" "wagtail" {
  name                = "${local.org}-${local.app}-id-${local.environment}"
  resource_group_name = data.azurerm_resource_group.wagtail.name
}

data "azurerm_cdn_frontdoor_profile" "wagtail" {
  name                = "${local.org}-${local.app}-afd-${local.environment}"
  resource_group_name = data.azurerm_resource_group.wagtail.name
}

data "azurerm_key_vault" "wagtail" {
  name                = "${local.org}-${local.short_app_name}-kv-app-${local.environment}-${local.region}"
  resource_group_name = data.azurerm_resource_group.wagtail.name
}
