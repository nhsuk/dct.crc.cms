data "azurerm_client_config" "current" {}

data "azurerm_key_vault" "kv" {
  name                = var.key_vault_name
  resource_group_name = var.key_vault_rg
}

resource "azurerm_role_assignment" "kv_reader" {
  scope                = data.azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Reader"
  principal_id         = data.azurerm_client_config.current.object_id
}

resource "azurerm_key_vault_access_policy" "terraform_sp_access" {
  key_vault_id = data.azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  secret_permissions = [
    "Get"
  ]
}

data "azurerm_key_vault_secret" "pubToken" {
  name         = "pubToken"
  key_vault_id = data.azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.terraform_sp_access, azurerm_role_assignment.kv_reader]
}
