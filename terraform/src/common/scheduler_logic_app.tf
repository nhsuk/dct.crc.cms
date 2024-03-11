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
        "parameters" : {},
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
        "actions" : {
          "Publish scheduled pages request" : {
            "inputs" : {
              "headers" : {
                "Authorization" : "Bearer ${data.azurerm_key_vault_secret.pubToken.value}"
              },
              "method" : "GET",
              "queries" : {},
              "uri" : var.publishing_endpoint
            },
            "runAfter" : {},
            "type" : "Http"
          },
          "Condition" : {
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
                          "text" : "See error detail: @body('Publish scheduled pages request')",
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
              }
            },
            "runAfter" : {
              "Publish scheduled pages request" : [
                "Failed",
                "Skipped",
                "TimedOut",
                "Succeeded"
              ]
            },
          }
        }
      }
    }
  })
}
