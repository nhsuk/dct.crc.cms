resource "azurerm_monitor_action_group" "activeconnections_alert" {
  count               = local.selected_environment != null ? 1 : 0
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-ag-")
  resource_group_name = data.azurerm_resource_group.rg.name
  short_name          = "ActiveConnAl"

  logic_app_receiver {
    name                    = "active_connections_slack_alert"
    resource_id             = azapi_resource.activeconnectionsalert_la[0].id
    callback_url            = jsondecode(data.azapi_resource_action.activeconnections_alert_la_callbackurl[0].output).value
    use_common_alert_schema = true
  }
}

resource "azurerm_monitor_metric_alert" "activeconnections_metric_alert_85" {
  count               = local.selected_environment != null ? 1 : 0
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnections-metricalert-85-")
  resource_group_name = data.azurerm_resource_group.rg.name
  scopes              = [local.postgresql_server_resource_id]
  description         = "Alert when active connections are greater than or equal to 85."
  severity            = 3
  frequency           = "PT1M"
  window_size         = "PT5M"
  enabled             = true

  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/servers"
    metric_name      = "active_connections"
    aggregation      = "Maximum"
    operator         = "GreaterThanOrEqual"
    threshold        = 85
  }

  action {
    action_group_id = azurerm_monitor_action_group.activeconnections_alert[0].id
  }
}

resource "azurerm_monitor_metric_alert" "activeconnections_metric_alert_98" {
  count               = local.selected_environment != null ? 1 : 0
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnections-metricalert-98-")
  resource_group_name = data.azurerm_resource_group.rg.name
  scopes              = [local.postgresql_server_resource_id]
  description         = "Alert when active connections are greater than or equal to 98."
  severity            = 2
  frequency           = "PT1M"
  window_size         = "PT5M"
  enabled             = true

  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/servers"
    metric_name      = "active_connections"
    aggregation      = "Maximum"
    operator         = "GreaterThanOrEqual"
    threshold        = 98
  }

  action {
    action_group_id = azurerm_monitor_action_group.activeconnections_alert[0].id
  }
}

resource "azurerm_monitor_metric_alert" "activeconnections_metric_alert_resolved" {  
  count               = local.selected_environment != null ? 1 : 0
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnections-metricalert-resolved-")  
  resource_group_name = data.azurerm_resource_group.rg.name  
  scopes              = [local.postgresql_server_resource_id]  
  description         = "Alert when active connections drop below 50"  
  severity            = 0 
  frequency           = "PT1M"  
  window_size         = "PT5M"  
  enabled             = true

  criteria {  
    metric_namespace = "Microsoft.DBforPostgreSQL/servers"  
    metric_name      = "active_connections"  
    aggregation      = "Maximum"  
    operator         = "LessThan"  
    threshold        = 50  
  }

  action {  
    action_group_id = azurerm_monitor_action_group.activeconnections_alert[0].id  
  }  
}

