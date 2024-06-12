resource "azurerm_key_vault_secret" "alerting_webhook" {
  name         = "alertingWebhook"
  value        = ""
  key_vault_id = azurerm_key_vault.kv.id
  lifecycle {
    ignore_changes = [value]
  }
}

resource "azurerm_key_vault_secret" "auth_token" {
  name         = "pubToken"
  value        = ""
  key_vault_id = azurerm_key_vault.kv.id
  lifecycle {
    ignore_changes = [value]
  }
}

resource "azurerm_key_vault_secret" "publishing_endpoint" {
  name         = "pubEndpoint"
  value        = ""
  key_vault_id = azurerm_key_vault.kv.id
  lifecycle {
    ignore_changes = [value]
  }
}

resource "azurerm_key_vault_secret" "search_index_endpoint" {
  name         = "searchIndexEndpoint"
  value        = ""
  key_vault_id = azurerm_key_vault.kv.id
  lifecycle {
    ignore_changes = [value]
  }
}
