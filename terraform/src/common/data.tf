/**
 * The resource group where all resources will be contained.
 * This terraform project doesn't create the resource group, the resource group
 * must already exist.
 */

data "azurerm_resource_group" "rg" {
  name = var.resource_group
}

data "azurerm_client_config" "current" {}

data "azurerm_log_analytics_workspace" "shared_log_analytics_workspace" {
  count    = 1
  provider = azurerm.law

  name                = local.law_name
  resource_group_name = local.law_resource_group_name
}

data "azurerm_container_app" "dr" {
  count = var.dr_deployed ? 1 : 0

  name                = "ca-haproxy-${var.env}-ukw"
  resource_group_name = replace(var.resource_group, "-uks", "-ukw")
}

data "azurerm_cdn_frontdoor_profile" "frontdoor" { # The frontdoor profile is only deployed to the primary region
  count = var.deploy_container_apps && var.location == "ukw" ? 1 : 0

  name                = "${local.org}-${local.app}-afd-${var.env}"
  resource_group_name = replace(var.resource_group, "-ukw", "-uks")
}
