resource "azapi_resource" "kv_connection" {
  type      = "Microsoft.Web/connections@2016-06-01"
  name      = replace(data.azurerm_resource_group.rg.name, "-rg-", "-keyvault-con-")
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  tags      = local.common_tags
  body = jsonencode({
    "properties" : {
      "displayName" : var.key_vault_name,
      "authenticatedUser" : {},
      "overallStatus" : "Ready",
      "statuses" : [
        {
          "status" : "Ready"
        }
      ],
      "connectionState" : "Enabled",
      "parameterValueSet" : {
        "name" : "oauthMI",
        "values" : {
          "vaultName" : {
            "value" : var.key_vault_name
          }
        }
      },
      "customParameterValues" : {},
      "createdTime" : "2023-02-27T18:21:05.3652827Z",
      "changedTime" : "2023-02-27T18:21:05.3652827Z",
      "api" : {
        "name" : data.azurerm_managed_api.kv.name,
        "displayName" : "Azure Key Vault",
        "description" : "Azure Key Vault is a service to securely store and access secrets.",
        "iconUri" : "https://connectoricons-prod.azureedge.net/releases/v1.0.1680/1.0.1680.3652/keyvault/icon.png",
        "brandColor" : "#0079d6",
        "category" : "Standard",
        "id" : data.azurerm_managed_api.kv.id,
        "type" : "Microsoft.Web/locations/managedApis"
      },
      "testLinks" : [],
      "testRequests" : []
    }
  })
}
