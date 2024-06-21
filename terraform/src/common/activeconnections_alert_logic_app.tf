resource "azapi_resource" "activeconnectionsalert_la" {  
  type      = "Microsoft.Logic/workflows@2019-05-01"  
  name      = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-la-")  
  location  = data.azurerm_resource_group.rg.location  
  parent_id = data.azurerm_resource_group.rg.id  
  tags      = local.common_tags

  identity {  
    type = "SystemAssigned"  
  }

  body = jsonencode({  
    "properties": {  
      "state": "Enabled",  
      "parameters" : {},
      "definition": {  
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",  
        "contentVersion": "1.0.0.0",  
        "parameters": {  
          "$connections": {  
            "defaultValue": {},  
            "type": "Object"  
          }
        },
        "actions": {  
          "Condition_Moderate": {  
            "actions": {  
              "SendModerateAlert": {  
                "inputs": {  
                  "body": templatefile("${path.module}/templates/activeconnections-moderate-slack-alert-body.tftpl", {  
                    rg_name = data.azurerm_resource_group.rg.name,  
                    rg_id = data.azurerm_resource_group.rg.id  
                  }),  
                  "headers": {  
                    "Content-Type": "application/json"  
                  },  
                  "method": "POST",  
                  "uri": "@{body('Get alerting webhook')?['value']}"  
                },  
                "runAfter": {},  
                "type": "Http"  
              }  
            },  
            "expression": {  
              "equals": [  
                "@triggerBody()?['data']?['alertContext']['condition']['allOf'][0]['metricValue']",  
                85  
              ]  
            },  
            "runAfter": {  
              "Get alerting webhook": [  
                "Succeeded"  
              ]  
            },  
            "type": "If"  
          },  
          "Condition_Severe": {  
            "actions": {  
              "SendSevereAlert": {  
                "inputs": {  
                  "body": templatefile("${path.module}/templates/activeconnections-severe-slack-alert-body.tftpl", {  
                    rg_name = data.azurerm_resource_group.rg.name,  
                    rg_id = data.azurerm_resource_group.rg.id  
                  }),  
                  "headers": {  
                    "Content-Type": "application/json"  
                  },  
                  "method": "POST",  
                  "uri": "@{body('Get alerting webhook')?['value']}"  
                },  
                "runAfter": {},  
                "type": "Http"  
              }  
            },  
            "expression": {  
              "equals": [  
                "@triggerBody()?['data']?['alertContext']['condition']['allOf'][0]['metricValue']",  
                98  
              ]  
            },  
            "runAfter": {  
              "Condition_Moderate": [  
                "Failed",  
                "Skipped",  
                "Succeeded"  
              ]  
            },  
            "type": "If"  
          },  
          "Get alerting webhook": {  
            "inputs": {  
              "host": {  
                "connection": {  
                  "name": "@parameters('$connections')['keyvault']['connectionId']"  
                }  
              },  
              "method": "get",  
              "path": "/secrets/@{encodeURIComponent('alertingWebhook')}/value"  
            },  
            "runAfter": {},  
            "type": "ApiConnection"  
          }  
        },  
        "parameters": {  
          "$connections": {  
            "value": {  
              "keyvault": {  
                "connectionId": azapi_resource.keyvault_con.id,  
                "connectionName": azapi_resource.keyvault_con.name,  
                "id": data.azurerm_managed_api.kv.id,  
                "connectionProperties": {  
                  "authentication": {  
                    "type": "ManagedServiceIdentity"  
                  }  
                }  
              }  
            }  
          }  
        },  
        "triggers": {  
          "manual": {  
            "type": "Request",  
            "kind": "Http",  
            "inputs": {  
              "schema": templatefile("${path.module}/schema/common-alert-schema.json", {})  
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
  depends_on  = [  
    azapi_resource.activeconnectionsalert_la  
  ]  
  response_export_values = ["value"]  
}
