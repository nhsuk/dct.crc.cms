resource "azurerm_monitor_metric_alert" "scheduler_fail_alert" {
  name                = format("Failing Runs - %s", azapi_resource.scheduler_la.name)
  resource_group_name = data.azurerm_resource_group.rg.name
  scopes              = [azapi_resource.scheduler_la.id]
  description         = "Action will be triggered when scheduler logic app run fails"
  window_size         = "PT1H"
  frequency           = "PT15M"
  severity            = 2

  criteria {
    metric_namespace = "Microsoft.Logic/workflows"
    metric_name      = "RunsFailed"
    aggregation      = "Count"
    operator         = "GreaterThanOrEqual"
    threshold        = 1
  }

  action {
    action_group_id = azurerm_monitor_action_group.scheduler_alert.id
  }
}