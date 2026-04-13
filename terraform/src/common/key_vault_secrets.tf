resource "azurerm_key_vault_secret" "wagtail" {
  # each dev instance gets it's own secrets copied as part of the deployment pipeline
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
