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
    properties : {
      parameters : {},
      state      : "Enabled",
      definition : {
        "$schema" : "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        actions   : {
          Condition_Moderate : {
            actions    : {
              SendModerateAlert : {
                inputs : {
                  body    : templatefile("${path.module}/templates/activeconnections-slack-alert-body.json.tftpl", { rg_name = data.azurerm_resource_group.rg.name, rg_id = data.azurerm_resource_group.rg.id, la_name = azapi_resource.activeconnectionsalert_la.name, la_id = azapi_resource.activeconnectionsalert_la.id }),
                  headers : {
                    "Content-Type" : "application/json"
                  },
                  method : "POST",
                  uri    : "@{body('Get alerting webhook')?['value']}"
                },
                runAfter : {},
                type     : "Http"
              }
            },
            expression : {
              equals : [
                "@triggerBody()?['data']?['alertContext']['condition']['allOf'][0]['metricValue']",
                85
              ]
            },
            runAfter : {
              "Get alerting webhook" : [
                "Succeeded"
              ]
            },
            type : "If"
          },
          Condition_Severe : {
            actions    : {
              SendSevereAlert : {
                inputs : {
                  body    : templatefile("${path.module}/templates/activeconnections-slack-alert-body.json.tftpl", { rg_name = data.azurerm_resource_group.rg.name, rg_id = data.azurerm_resource_group.rg.id, la_name = azapi_resource.activeconnectionsalert_la.name, la_id = azapi_resource.activeconnectionsalert_la.id }),
                  headers : {
                    "Content-Type" : "application/json"
                  },
                  method : "POST",
                  uri    : "@{body('Get alerting webhook')?['value']}"
                },
                runAfter : {},
                type     : "Http"
              }
            },
            expression : {
              equals : [
                "@triggerBody()?['data']?['alertContext']['condition']['allOf'][0]['metricValue']",
                98
              ]
            },
            runAfter : {
              Condition_Moderate : [
                "Failed",
                "Skipped",
                "Succeeded"
              ]
            },
            type : "If"
          },
          "Get alerting webhook" : {
            inputs : {
              host : {
                connection : {
                  name : "@parameters('$connections')['keyvault']['connectionId']"
                }
              },
              method : "get",
              path   : "/secrets/@{encodeURIComponent('alertingWebhook')}/value"
            },
            runAfter : {},
            type     : "ApiConnection"
          }
        },
        contentVersion : "1.0.0.0",
        parameters     : {
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
        },
        triggers : {
          manual : {
            inputs : {
              schema : {
                properties : {
                  data : {
                    properties : {
                      alertContext : {
                        properties : {
                          condition : {
                            properties : {
                              allOf : {
                                items : {
                                  properties : {
                                    metricValue : {
                                      type : "number"
                                    }
                                  },
                                  required : [
                                    "metricValue"
                                  ]
                                },
                                type : "array"
                              }
                            }
                          }
                        },
                        type : "object"
                      },
                      essentials : {
                        properties : {
                          alertContextVersion : {
                            type : "string"
                          },
                          alertId : {
                            type : "string"
                          },
                          alertRule : {
                            type : "string"
                          },
                          alertTargetIDs : {
                            items : {
                              type : "string"
                            },
                            type : "array"
                          },
                          description : {
                            type : "string"
                          },
                          essentialsVersion : {
                            type : "string"
                          },
                          firedDateTime : {
                            type : "string"
                          },
                          monitorCondition : {
                            type : "string"
                          },
                          monitoringService : {
                            type : "string"
                          },
                          originAlertId : {
                            type : "string"
                          },
                          resolvedDateTime : {
                            type : "string"
                          },
                          severity : {
                            type : "string"
                          },
                          signalType : {
                            type : "string"
                          }
                        },
                        type : "object"
                      }
                    },
                    type : "object"
                  },
                  schemaId : {
                    type : "string"
                  }
                },
                type : "object"
              }
            },
            kind : "Http",
            type : "Request"
          }
        }
      }
    },
    parameters : {
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
