resource "azurerm_key_vault_secret" "postgresql_admin_user" {
  #checkov:skip=CKV_AZURE_41 Expiration date not required
  #checkov:skip=CKV_AZURE_114 Content type on secret not used
  name         = "postgresqlAdminUser"
  value        = azurerm_postgresql_flexible_server.database.administrator_login
  key_vault_id = var.key_vault.id
}

resource "azurerm_key_vault_secret" "postgresql_admin_password" {
  #checkov:skip=CKV_AZURE_41 Expiration date not required
  #checkov:skip=CKV_AZURE_114 Content type on secret not used
  name         = "postgresqlAdminPassword"
  value        = azurerm_postgresql_flexible_server.database.administrator_password
  key_vault_id = var.key_vault.id
}
