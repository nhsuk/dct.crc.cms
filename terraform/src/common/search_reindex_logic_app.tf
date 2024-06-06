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
          "When_a_HTTP_request_is_received": {
            "type": "Request",
            "kind": "Http"
          },
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
              "Get index endpoint" : {
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
              "Get publishing token" : {
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
                  "Get index endpoint" : [
                    "Succeeded"
                  ]
                },
                "type" : "ApiConnection"
              },
              "Publish scheduled pages request" : {
                "inputs" : {
                  "headers" : {
                    "Authorization" : "Bearer @{body('Get publishing token')?['value']}"
                  },
                  "method" : "GET",
                  "queries" : {},
                  "uri" : "@{body('Get index endpoint')?['value']}"
                },
                "runAfter" : {
                  "Get publishing token" : [
                    "Succeeded"
                  ]
                },
                "type" : "Http"
              }
            },
            "runAfter" : {},
            "type" : "Scope"
          },
          "Check" : {
            "type" : "If",
            "expression" : {
              "and" : [
                {
                  "not" : {
                    "equals" : [
                      "@outputs('Publish scheduled pages request')['statusCode']",
                      202
                    ]
                  }
                }
              ]
            },
            "actions" : {
              "Terminate" : {
                "inputs" : {
                  "runError" : {
                    "message" : "Publishing scheduled pages failed"
                  },
                  "runStatus" : "Failed"
                },
                "runAfter" : {},
                "type" : "Terminate"
              }
            },
            "runAfter" : {
              "Publish" : [
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
