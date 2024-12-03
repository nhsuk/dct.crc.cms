resource "azapi_resource" "scheduler_la" {
  type      = "Microsoft.Logic/workflows@2019-05-01"
  name      = local.scheduler_logic_app_name
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
          "Publish scheduled pages trigger" : {
            "evaluatedRecurrence" : {
              "frequency" : "Day",
              "interval" : 1,
              "schedule" : {
                "hours" : [
                  "0",
                  "1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23"
                ],
                "minutes" : [
                  5
                ]
              }
            },
            "recurrence" : {
              "frequency" : "Day",
              "interval" : 1,
              "schedule" : {
                "hours" : [
                  "0",
                  "1",
                  "2",
                  "3",
                  "4",
                  "5",
                  "6",
                  "7",
                  "8",
                  "9",
                  "10",
                  "11",
                  "12",
                  "13",
                  "14",
                  "15",
                  "16",
                  "17",
                  "18",
                  "19",
                  "20",
                  "21",
                  "22",
                  "23"
                ],
                "minutes" : [
                  5
                ]
              }
            },
            "type" : "Recurrence"
          }
        },
        "actions" : {
          "Publish" : {
            "actions" : {
              "Get publishing endpoint" : {
                "inputs" : {
                  "host" : {
                    "connection" : {
                      "name" : "@parameters('$connections')['keyvault']['connectionId']"
                    }
                  },
                  "method" : "get",
                  "path" : "/secrets/@{encodeURIComponent('pubEndpoint')}/value"
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
                  "Get publishing endpoint" : [
                    "Succeeded"
                  ]
                },
                "type" : "ApiConnection"
              },
              "Get Basic Auth" : {
                "inputs" : {
                  "host" : {
                    "connection" : {
                      "name" : "@parameters('$connections')['keyvault']['connectionId']"
                    }
                  },
                  "method" : "get",
                  "path" : "/secrets/@{encodeURIComponent('basicAuth')}/value"
                },
                "runAfter" : {
                  "Get publishing token" : [
                    "Succeeded"
                  ]
                },
                "type" : "ApiConnection"
              },
              "Publish scheduled pages request" : {
                "inputs" : {
                  "authentication" : {
                    "type" : "Raw",
                    "value" : "Basic @{body('Get Basic Auth')?['value']}"
                  },
                  "headers" : {
                    "AdminToken" : "@{body('Get publishing token')?['value']}"
                  },
                  "method" : "GET",
                  "queries" : {},
                  "uri" : "@{body('Get publishing endpoint')?['value']}"
                },
                "runAfter" : {
                  "Get Stag Auth" : [
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
