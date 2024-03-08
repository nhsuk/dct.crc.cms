resource "azapi_resource" "publisher_la" {
  type      = "Microsoft.Logic/workflows@2019-05-01"
  name      = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduler-la-")
  location  = data.azurerm_resource_group.rg.location
  parent_id = data.azurerm_resource_group.rg.id
  tags      = local.common_tags
  body = jsonencode({
    "type" : "Microsoft.Logic/workflows",
    "apiVersion" : "2017-07-01",
    "name" : "${replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduler-la-")}",
    "location" : "${data.azurerm_resource_group.rg.location}",
    "identity" : {
      "type" : "SystemAssigned"
    },
    "properties" : {
      "state" : "Disabled",
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
          "Publishing_trigger" : {
            "recurrence" : {
              "frequency" : "Minute",
              "interval" : 15
            },
            "evaluatedRecurrence" : {
              "frequency" : "Minute",
              "interval" : 15
            },
            "type" : "Recurrence"
          }
        },
        "actions" : {
          "Get_publishing_token" : {
            "runAfter" : {},
            "type" : "ApiConnection",
            "inputs" : {
              "host" : {
                "connection" : {
                  "name" : "{@parameters('$connections')['keyvault']['connectionId']}"
                }
              },
              "method" : "get",
              "path" : "/secrets/@{encodeURIComponent('pubToken')}/value"
            }
          },
          "Request_publishing" : {
            "runAfter" : {
              "Get_publishing_token" : [
                "Succeeded"
              ]
            },
            "type" : "Http",
            "inputs" : {
              "headers" : {
                "Authorization" : "Bearer @{body('Get_publishing_token')?['value']}"
              },
              "method" : "GET",
              "uri" : "${var.publishing_endpoint}"
            }
          },
          "outputs" : {}
        },
        "parameters" : {
          "$connections" : {
            "value" : {
              "keyvault" : {
                "connectionId" : "${azapi_resource.kv_connection.id}",
                "connectionName" : "${azapi_resource.kv_connection.name}",
                "connectionProperties" : {
                  "authentication" : {
                    "type" : "ManagedServiceIdentity"
                  }
                },
                "id" : "${data.azurerm_managed_api.kv.id}"
              }
            }
          }
        }
      }
    }
  })
}
