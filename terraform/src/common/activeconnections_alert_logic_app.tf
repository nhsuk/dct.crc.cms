resource "azapi_resource" "activeconnectionsalert_la" {
  type      = "Microsoft.Logic/workflows@2019-05-01"
  name      = local.activeconnections_logic_app_name
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  tags      = local.common_tags

  identity {
    type = "SystemAssigned"
  }

  body = jsonencode({
    "properties" : {
      "state" : var.environment == "development" ? "Disabled" : "Enabled",
      "parameters" : {},
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
              "path" : "/secrets/@{encodeURIComponent('alertingWebhook')}/value"
            },
            "runAfter" : {},
            "type" : "ApiConnection"
          },
          "SendAlert" : {
            "inputs" : {
              "body" : templatefile("${path.module}/templates/activeconnections-slack-alert-body.tftpl", {
                rg_name                = data.azurerm_resource_group.rg.name,
                rg_id                  = data.azurerm_resource_group.rg.id,
                la_name                = local.activeconnections_logic_app_name,
                la_id                  = local.activeconnections_logic_app_id,
                postgresql_server_name = data.azurerm_postgresql_flexible_server.flex.name,
                postgresql_server_id   = data.azurerm_postgresql_flexible_server.flex.id
              }),
              "headers" : {
                "Content-Type" : "application/json"
              },
              "method" : "POST",
              "uri" : "@{body('Get alerting webhook')?['value']}"
            },
            "runAfter" : {
              "Get alerting webhook" : [
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

data "azapi_resource_action" "activeconnections_alert_la_callbackurl" {
  resource_id = "${azapi_resource.activeconnectionsalert_la.id}/triggers/manual"
  action      = "listCallbackUrl"
  type        = "Microsoft.Logic/workflows/triggers@2018-07-01-preview"
  depends_on = [
    azapi_resource.activeconnectionsalert_la
  ]
  response_export_values = ["value"]
}