locals {
  config_key_vault_name      = var.env != "prod" ? "dct-config-kv-int-uks" : "dct-config-kv-prod-uks"
  config_resource_group_name = var.env != "prod" ? "dct-config-rg-int-uks" : "dct-config-rg-prod-uks"
}

data "azurerm_key_vault" "dct_config_key_vault" {
  name                = local.config_key_vault_name
  resource_group_name = local.config_resource_group_name
}

data "azurerm_key_vault_secret" "budget_alert_email" {
  name         = "campaigns-monitoring-email"
  key_vault_id = data.azurerm_key_vault.dct_config_key_vault.id
}