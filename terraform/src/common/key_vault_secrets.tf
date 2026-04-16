resource "azurerm_key_vault_secret" "wagtail" {
  #checkov:skip=CKV_AZURE_41 Expiration date not required
  #checkov:skip=CKV_AZURE_114 Content type on secret not used
  # each dev instance gets its own secrets copied as part of the deployment pipeline
  for_each = var.env != "dev" ? toset(concat(local.app_secrets, local.init_secrets)) : toset([])

  name         = replace(lower(each.key), "_", "-")
  value        = "EMPTY"
  key_vault_id = module.container_app_env[0].key_vault_id

  lifecycle {
    ignore_changes = [value, tags]
  }
}

moved {
  from = module.aca_wagtail[0].azurerm_key_vault_secret.wagtail
  to   = azurerm_key_vault_secret.wagtail
}
