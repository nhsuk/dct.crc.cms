resource "azurerm_monitor_action_group" "scheduler_alert" {
  name                = replace(data.azurerm_resource_group.rg.name, "-rg-", "-scheduleralert-ag-")
  resource_group_name = data.azurerm_resource_group.rg.name
  short_name          = "ScheduleFail"

  logic_app_receiver {
    name                    = "scheduler slack alert"
    resource_id             = azapi_resource.scheduler_alert_la.id
    callback_url            = jsonencode(azapi_resource.scheduler_alert_la.output).properties.callback_url
    use_common_alert_schema = true
  }
}
