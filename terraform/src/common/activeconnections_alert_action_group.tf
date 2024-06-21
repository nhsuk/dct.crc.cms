data "azurerm_postgresql_server" "postgres_server" {  
  name                = var.postgresql_server
  resource_group_name = data.azurerm_resource_group.rg.name  
}

resource "azurerm_monitor_action_group" "activeconnections_alert" {  
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-ag-")  
  resource_group_name = data.azurerm_resource_group.rg.name  
  short_name          = "ActiveConnections"

  logic_app_receiver {  
    name                    = "active_connections_slack_alert"  
    resource_id             = azapi_resource.activeconnectionsalert_la.id  
    callback_url            = jsondecode(data.azurerm_resource_action.activeconnections_alert_la_callbackurl.response).value  
    use_common_alert_schema = true  
  }  
}

resource "azurerm_monitor_metric_alert" "activeconnections_metric_alert" {  
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnections-metricalert-")  
  resource_group_name = data.azurerm_resource_group.rg.name  
  scopes              = [data.azurerm_postgresql_server.postgres_server.id]  
  description         = "Alert when active connections are greater than or equal to 85."  
  severity            = 3  
  frequency           = "PT1M"  
  window_size         = "PT5M"  
  enabled             = true

  criteria {  
    metric_namespace = "Microsoft.DBforPostgreSQL/servers"  
    metric_name      = "active_connections"  
    aggregation      = "Total"  
    operator         = "GreaterThanOrEqual"  
    threshold        = 85  
  }

  action {  
    action_group_id = azurerm_monitor_action_group.activeconnections_alert.id  
  }  
}
