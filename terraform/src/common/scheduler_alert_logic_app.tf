resource "azapi_resource" "scheduler_alert_la" {
  type      = "Microsoft.Logic/workflows@2019-05-01"
  name      = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduleralert-la-")
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  tags      = local.common_tags
  identity {
    type = "SystemAssigned"
  }
  body = jsonencode({
    "properties" : {
      "parameters" : {},
      "state" : "Enabled",
      "definition" : {
        "$schema" : "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "contentVersion" : "1.0.0.0",
        "parameters" : {
          "$connections" : {
            "defaultValue" : {},
            "type" : "Object"
          }
        },
        "triggers" : {
          "manual" : {
            "type" : "Request",
            "kind" : "Http",
            "inputs" : {
              "schema" : templatefile("${path.module}/schema/common-alert-schema.json", {})
            }
          }
        },
        "actions" : {
          "Get alerting webhook" : {
            "inputs" : {
              "host" : {
                "connection" : {
                  "name" : "@parameters('$connections')['keyvault']['connectionId']"
                }
              },
              "method" : "get",
              "path" : "/secrets/@{encodeURIComponent('${azurerm_key_vault_secret.secrets["alertingWebhook"].name}')}/value"
            },
            "runAfter" : {},
            "type" : "ApiConnection"
          },
          "Get publishing endpoint" : {
            "inputs" : {
              "host" : {
                "connection" : {
                  "name" : "@parameters('$connections')['keyvault']['connectionId']"
                }
              },
              "method" : "get",
              "path" : "/secrets/@{encodeURIComponent('${azurerm_key_vault_secret.secrets["pubEndpoint"].name}')}/value"
            },
            "runAfter" : {
              "Get alerting webhook" : [
                "Succeeded"
              ]
            },
            "type" : "ApiConnection"
          },
          "Send slack alert" : {
            "inputs" : {
              "body" : templatefile("${path.module}/templates/slack-alert-body.json.tftpl", { rg_name = data.azurerm_resource_group.rg.name, rg_id = data.azurerm_resource_group.rg.id, la_name = azapi_resource.scheduler_la.name, la_id = azapi_resource.scheduler_la.id }),
              "headers" : {
                "Content-Type" : "application/json"
              },
              "method" : "POST",
              "uri" : "@{body('Get alerting webhook')?['value']}"
            },
            "runAfter" : {
              "Get publishing endpoint" : [
                "Failed",
                "Skipped",
                "TimedOut",
                "Succeeded"
              ]
            },
            "type" : "Http"
          }
        }
      },
      "parameters" : {
        "$connections" : {
          "value" : {
            "keyvault" : {
              "connectionId" : azapi_resource.keyvault_con.id,
              "connectionName" : azapi_resource.keyvault_con.name,
              "id" : data.azurerm_managed_api.kv.id,
              "connectionProperties" : {
                "authentication" : {
                  "type" : "ManagedServiceIdentity"
                }
              }
            }
          }
        }
      }
    }
  })
}

data "azapi_resource_action" "scheduler_alert_la_callbackurl" {
  resource_id = "${azapi_resource.scheduler_alert_la.id}/triggers/manual"
  action      = "listCallbackUrl"
  type        = "Microsoft.Logic/workflows/triggers@2018-07-01-preview"
  depends_on = [
    azapi_resource.scheduler_alert_la
  ]
  response_export_values = ["value"]
}
