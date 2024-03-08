resource "azurerm_logic_app_trigger_recurrence" "publish_scheduled_pages_trigger" {
  name         = "Publish scheduled pages trigger"
  logic_app_id = azurerm_logic_app_workflow.publish_scheduled_pages_workflow.id
  interval     = 15
  frequency    = "Minute"
}