data "azurerm_client_config" "current" {}

data "azurerm_key_vault" "kv" {
  name                = var.key_vault_name
  resource_group_name = var.key_vault_rg
}

data "azurerm_key_vault_secret" "pubToken" {
  name         = "pubToken"
  key_vault_id = data.azurerm_key_vault.kv.id
  depends_on   = [azurerm_key_vault_access_policy.terraform_sp_access, azurerm_role_assignment.kv_reader]
}
