resource "azapi_resource" "scheduler_la" {
  type      = "Microsoft.Logic/workflows@2019-05-01"
  name      = local.scheduler_logic_app_name
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  tags      = local.common_tags
  body = jsonencode({
    "identity" : {
      "type" : "SystemAssigned"
    },
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
              "frequency" : "Minute",
              "interval" : 15
            },
            "recurrence" : {
              "frequency" : "Minute",
              "interval" : 15
            },
            "type" : "Recurrence"
          }
        },
        "Publish" : {
          "actions" : {
            "Get publishing secret" : {
              "inputs" : {
                "host" : {
                  "connection" : {
                    "name" : "@parameters('$connections')['keyvault']['connectionId']"
                  }
                },
                "method" : "get",
                "path" : "/secrets/@{encodeURIComponent('pubToken')}/value"
              },
              "runAfter" : {},
              "type" : "ApiConnection"
            },
            "Publish scheduled pages request" : {
              "inputs" : {
                "headers" : {
                  "Authorization" : "Bearer @{body('Get publishing secret')?['value']}"
                },
                "method" : "GET",
                "queries" : {},
                "uri" : var.publishing_endpoint
              },
              "runAfter" : {
                "Get publishing secret" : [
                  "Succeeded"
                ]
              },
              "type" : "Http"
            },
            "runAfter" : {},
            "type" : "Scope"
          }
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
              "Send slack alert" : {
                "inputs" : {
                  "body" : {
                    "blocks" : [
                      {
                        "text" : {
                          "text" : "CRCv3 Publishing Of Scheduled Pages Failure",
                          "type" : "plain_text"
                        },
                        "type" : "header"
                      },
                      {
                        "text" : {
                          "text" : "Request failed with status code @{outputs('Publish scheduled pages request')['statusCode']}",
                          "type" : "mrkdwn"
                        },
                        "type" : "section"
                      },
                      {
                        "text" : {
                          "text" : "*Logic App*\n <https://portal.azure.com/#@nhschoices.net/resource${data.azurerm_resource_group.rg.id}/providers/Microsoft.Logic/workflows/${local.scheduler_logic_app_name}/logicApp|${local.scheduler_logic_app_name}>",
                          "type" : "mrkdwn"
                        },
                        "type" : "section"
                      },
                      {
                        "text" : {
                          "text" : "*Resource Group*\n <https://portal.azure.com/#@nhschoices.net/resource${data.azurerm_resource_group.rg.id}|${data.azurerm_resource_group.rg.name}>",
                          "type" : "mrkdwn"
                        },
                        "type" : "section"
                      },
                      {
                        "text" : {
                          "text" : "*Publishing Endpoint*\n ${var.publishing_endpoint}",
                          "type" : "mrkdwn"
                        },
                        "type" : "section"
                      }
                    ]
                  },
                  "headers" : {
                    "Content-Type" : "application/json"
                  },
                  "method" : "POST",
                  "uri" : var.campaigns_monitoring_webhook
                },
                "runAfter" : {},
                "type" : "Http"
              },
              "Terminate" : {
                "inputs" : {
                  "runError" : {
                    "message" : "Publishing request was not accepted"
                  },
                  "runStatus" : "Failed"
                },
                "runAfter" : {
                  "Send slack alert" : [
                    "Failed",
                    "Skipped",
                    "TimedOut",
                    "Succeeded"
                  ]
                },
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
            },
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
