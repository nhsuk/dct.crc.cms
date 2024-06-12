data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = local.key_vault_name
  location                    = data.azurerm_resource_group.rg.location
  resource_group_name         = data.azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  purge_protection_enabled    = false
  sku_name                    = "standard"

  access_policy {
    tenant_id = azapi_resource.scheduler_la.identity[0].tenant_id
    object_id = azapi_resource.scheduler_la.identity[0].principal_id
    secret_permissions = [
      "Get", "List"
    ]
  }
  
  access_policy {
    tenant_id = azapi_resource.scheduler_alert_la.identity[0].tenant_id
    object_id = azapi_resource.scheduler_alert_la.identity[0].principal_id
    secret_permissions = [
      "Get", "List"
    ]
  }

  access_policy {
    tenant_id = azapi_resource.search_reindex_la.identity[0].tenant_id
    object_id = azapi_resource.search_reindex_la.identity[0].principal_id
    secret_permissions = [
      "Get", "List"
    ]
  }

  lifecycle {
    ignore_changes = [
      access_policy
    ]
  }
}
