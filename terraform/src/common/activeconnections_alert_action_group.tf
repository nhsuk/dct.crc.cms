resource "azurerm_monitor_action_group" "activeconnections_alert" {
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnectionsalert-ag-")
  resource_group_name = data.azurerm_resource_group.rg.name
  short_name          = "ActiveConnAl"

  logic_app_receiver {
    name                    = "active_connections_slack_alert"
    resource_id             = azapi_resource.activeconnectionsalert_la.id
    callback_url            = data.azapi_resource_action.activeconnections_alert_la_callbackurl.output.value
    use_common_alert_schema = true
  }
}

resource "azurerm_monitor_metric_alert" "activeconnections_metric_alert_85" {
  name                 = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnections-metricalert-85-")
  resource_group_name  = data.azurerm_resource_group.rg.name
  scopes               = [local.postgres_flex_id]
  target_resource_type = "Microsoft.DBforPostgreSQL/flexibleServers"
  description          = "Alert when active connections are greater than or equal to 85."
  severity             = 2
  frequency            = "PT1M"
  window_size          = "PT5M"
  enabled              = true

  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
    metric_name      = "active_connections"
    aggregation      = "Maximum"
    operator         = "GreaterThanOrEqual"
    threshold        = 85
  }

  action {
    action_group_id = azurerm_monitor_action_group.activeconnections_alert.id
  }
}

resource "azurerm_monitor_metric_alert" "activeconnections_metric_alert_98" {
  name                 = replace(data.azurerm_resource_group.rg.name, "-rg-", "-activeconnections-metricalert-98-")
  resource_group_name  = data.azurerm_resource_group.rg.name
  scopes               = [local.postgres_flex_id]
  target_resource_type = "Microsoft.DBforPostgreSQL/flexibleServers"
  description          = "Alert when active connections are greater than or equal to 98."
  severity             = 0
  frequency            = "PT1M"
  window_size          = "PT5M"
  enabled              = true

  criteria {
    metric_namespace = "Microsoft.DBforPostgreSQL/flexibleServers"
    metric_name      = "active_connections"
    aggregation      = "Maximum"
    operator         = "GreaterThanOrEqual"
    threshold        = 98
  }

  action {
    action_group_id = azurerm_monitor_action_group.activeconnections_alert.id
  }
}