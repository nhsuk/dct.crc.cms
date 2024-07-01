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
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id
    secret_permissions = [
      "Get", "List", "Set", "Delete", "Purge"
    ]
  }

  dynamic "access_policy" {
    for_each = var.environment == "development" ? [1] : []
    content {
      tenant_id = data.azurerm_client_config.current.tenant_id
      object_id = "8c147d05-8d42-4dbb-8ddd-c466d1fc5210" # "AZURE_Development_Contributors" Azure Entra Group Object Id
      secret_permissions = [
        "Get", "List", "Set", "Delete", "Purge", "Backup", "Recover", "Restore"
      ]
    }
  }

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

  dynamic "access_policy" {
    for_each = var.environment != "development" ? [1] : []
    content {
      tenant_id = azapi_resource.activeconnectionsalert_la[0].identity[0].tenant_id
      object_id = azapi_resource.activeconnectionsalert_la[0].identity[0].principal_id
      secret_permissions = [
        "Get", "List"
      ]
    }
  }
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
