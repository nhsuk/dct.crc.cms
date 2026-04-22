resource "azurerm_key_vault" "kv" {
  #checkov:skip=CKV_AZURE_109 Key vault access from public networks to support ADO hosted agents
  #checkov:skip=CKV_AZURE_189 Key vault access from public networks to support ADO hosted agents
  #checkov:skip=CKV_AZURE_110 No purge protection required as secret values managed by terraform
  #checkov:skip=CKV_AZURE_42 No key vault protection required as secret values managed by terraform
  #checkov:skip=CKV2_AZURE_32 No private endpoint yet
  name                      = local.key_vault_name
  location                  = data.azurerm_resource_group.rg.location
  resource_group_name       = data.azurerm_resource_group.rg.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  enable_rbac_authorization = true
}

resource "azurerm_role_assignment" "key_vault_pipeline_identity" {
  principal_id         = data.azurerm_client_config.current.object_id
  role_definition_name = "Key Vault Secrets Officer"
  scope                = azurerm_key_vault.kv.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "scheduler_la_identity" {
  principal_id         = azapi_resource.scheduler_la.identity[0].principal_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.kv.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "search_reindex_la_identity" {
  principal_id         = azapi_resource.search_reindex_la.identity[0].principal_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.kv.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "activeconnectionsalert_la_identity" {
  principal_id         = azapi_resource.activeconnectionsalert_la.identity[0].principal_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.kv.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_key_vault_secret" "secrets" {
  #checkov:skip=CKV_AZURE_41 Expiration date not required
  #checkov:skip=CKV_AZURE_114 Content type on secret not used
  for_each     = toset(local.secret_names)
  name         = each.key
  value        = ""
  key_vault_id = azurerm_key_vault.kv.id
  lifecycle {
    ignore_changes = [value]
  }
  depends_on = [azurerm_role_assignment.key_vault_pipeline_identity]
}
