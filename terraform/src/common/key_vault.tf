data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = local.key_vault_name
  location                    = data.azurerm_resource_group.rg.location
  resource_group_name         = data.azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  purge_protection_enabled    = false
  sku_name                    = "standard"
  lifecycle {
    ignore_changes = [
      access_policy
    ]
  }
}

resource "azurerm_key_vault_access_policy" "terraform_kv_policy" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id
  secret_permissions = [
    "Get", "Set"
  ]
}

resource "azurerm_key_vault_access_policy" "scheduler_kv_policy" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = azapi_resource.scheduler_la.identity[0].tenant_id
  object_id    = azapi_resource.scheduler_la.identity[0].principal_id
  secret_permissions = [
    "Get", "List"
  ]
}

resource "azurerm_key_vault_access_policy" "scheduler_alert_kv_policy" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = azapi_resource.scheduler_alert_la.identity[0].tenant_id
  object_id    = azapi_resource.scheduler_alert_la.identity[0].principal_id
  secret_permissions = [
    "Get", "List"
  ]
}

resource "azurerm_key_vault_access_policy" "search_reindex_kv_policy" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = azapi_resource.search_reindex_la.identity[0].tenant_id
  object_id    = azapi_resource.search_reindex_la.identity[0].principal_id
  secret_permissions = [
    "Get", "List"
  ]
}

resource "azurerm_key_vault_secret" "secrets" {
  for_each     = toset(local.secret_names)
  name         = each.key
  value        = ""
  key_vault_id = azurerm_key_vault.kv.id
  lifecycle {
    ignore_changes = [value]
  }
}
