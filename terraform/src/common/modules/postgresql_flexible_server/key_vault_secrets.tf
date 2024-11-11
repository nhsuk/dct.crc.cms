resource "azurerm_key_vault_secret" "postgresql_admin_user" {
  name         = "postgresqlAdminUser"
  value        = azurerm_postgresql_flexible_server.database.administrator_login
  key_vault_id = var.key_vault.id
}

resource "azurerm_key_vault_secret" "postgresql_admin_password" {
  name         = "postgresqlAdminPassword"
  value        = azurerm_postgresql_flexible_server.database.administrator_password
  key_vault_id = var.key_vault.id
}
