resource "azapi_resource" "search_reindex_la" {
  type      = "Microsoft.Logic/workflows@2019-05-01"
  name      = local.search_reindex_logic_app_name
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  tags      = local.common_tags
  identity {
    type = "SystemAssigned"
  }
  body = jsonencode({
    "properties" : {
      "parameters" : {},
      "state" : "${var.environment == "development" ? "Disabled" : "Enabled"}",
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
          "Recurrence": {
            "type": "Recurrence",
            "recurrence": {
              "interval": 1,
              "frequency": "Day",
              "timeZone": "GMT Standard Time",
              "schedule": {
                "hours": [
                  "4"
                ]
              }
            }
          }
        },
        "actions" : {
          "Re-Index" : {
            "actions" : {
              "Get Endpoint" : {
                "inputs" : {
                  "host" : {
                    "connection" : {
                      "name" : "@parameters('$connections')['keyvault']['connectionId']"
                    }
                  },
                  "method" : "get",
                  "path" : "/secrets/@{encodeURIComponent('searchIndexEndpoint')}/value"
                },
                "runAfter" : {},
                "type" : "ApiConnection"
              },
              "Get Token" : {
                "inputs" : {
                  "host" : {
                    "connection" : {
                      "name" : "@parameters('$connections')['keyvault']['connectionId']"
                    }
                  },
                  "method" : "get",
                  "path" : "/secrets/@{encodeURIComponent('pubToken')}/value"
                },
                "runAfter" : {
                  "Get Endpoint" : [
                    "Succeeded"
                  ]
                },
                "type" : "ApiConnection"
              },
              "Trigger Re-Index" : {
                "inputs" : {
                  "authentication": {
                    "type": "Raw",
                    "value": "Bearer @{body('Get Token')?['value']}"
                  }
                  "method" : "GET",
                  "queries" : {},
                  "uri" : "@{body('Get Endpoint')?['value']}"
                },
                "runAfter" : {
                  "Get Token" : [
                    "Succeeded"
                  ]
                },
                "type" : "Http",
                "runtimeConfiguration": {
                  "contentTransfer": {
                    "transferMode": "Chunked"
                  }
                }
              }
            },
            "runAfter" : {},
            "type" : "Scope"
          },
          "Check" : {
            "type" : "scope",
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
              "Send slack alert" : {
                "inputs" : {
                  "body" : templatefile("${path.module}/templates/slack-alert-reindex.json.tftpl", { rg_name = data.azurerm_resource_group.rg.name, rg_id = data.azurerm_resource_group.rg.id, la_name = azapi_resource.scheduler_la.name, la_id = azapi_resource.scheduler_la.id }),
                  "headers" : {
                    "Content-Type" : "application/json"
                  },
                  "method" : "POST",
                  "uri" : "@{body('Get alerting webhook')?['value']}"
                },
             
                "type" : "Http", 
                "runAfter": {
                  "Get alerting webhook" : [
                    "Succeeded"
                  ]
                }
              }
            },
            "runAfter" : {
              "Re-Index" : [
                "Failed",
                "Skipped",
                "TimedOut",
                "Succeeded"
              ]
            }
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
