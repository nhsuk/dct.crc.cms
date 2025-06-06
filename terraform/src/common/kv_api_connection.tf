data "azurerm_managed_api" "kv" {
  name     = "keyvault"
  location = data.azurerm_resource_group.rg.location
}

resource "azapi_resource" "keyvault_con" {
  type                      = "Microsoft.Web/connections@2016-06-01"
  name                      = replace(data.azurerm_resource_group.rg.name, "-rg-", "-keyvault-con-")
  location                  = data.azurerm_resource_group.rg.location
  parent_id                 = data.azurerm_resource_group.rg.id
  schema_validation_enabled = false
  tags                      = local.common_tags
  body = {
    properties = {
      displayName = local.key_vault_name
      parameterValueSet = {
        name = "oauthMI"
        values = {
          vaultName = {
            "value" = local.key_vault_name
          }
        }
      }
      api = {
        name        = data.azurerm_managed_api.kv.name
        displayName = "Azure Key Vault"
        description = "Azure Key Vault is a service to securely store and access secrets."
        iconUri     = "https://connectoricons-prod.azureedge.net/releases/v1.0.1680/1.0.1680.3652/keyvault/icon.png"
        brandColor  = "#0079d6"
        id          = data.azurerm_managed_api.kv.id
      }
    }
  }
  lifecycle {
    ignore_changes = [
      body.properties.api.iconUri,
      body.properties.api.brandColor
    ]
  }
}
