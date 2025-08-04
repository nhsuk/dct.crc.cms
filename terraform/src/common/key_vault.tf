#trivy:ignore:avd-azu-0016 no purge protection required
#trivy:ignore:avd-azu-0013 enable access from public networks to support ADO hosted agents
resource "azurerm_key_vault" "kv_2" {
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
  scope                = azurerm_key_vault.kv_2.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "scheduler_la_identity" {
  principal_id         = azapi_resource.scheduler_la.identity[0].principal_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.kv_2.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "search_reindex_la_identity" {
  principal_id         = azapi_resource.search_reindex_la.identity[0].principal_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.kv_2.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_role_assignment" "activeconnectionsalert_la_identity" {
  principal_id         = azapi_resource.activeconnectionsalert_la.identity[0].principal_id
  role_definition_name = "Key Vault Secrets User"
  scope                = azurerm_key_vault.kv_2.id
  principal_type       = "ServicePrincipal"
}

resource "azurerm_key_vault_secret" "secrets_2" {
  for_each     = toset(local.secret_names)
  name         = each.key
  value        = ""
  key_vault_id = azurerm_key_vault.kv_2.id
  lifecycle {
    ignore_changes = [value]
  }
}
