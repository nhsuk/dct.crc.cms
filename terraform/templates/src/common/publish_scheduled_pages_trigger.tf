resource "azurerm_logic_app_trigger_recurrence" "publish_scheduled_pages_trigger" {
  name         = "Publish scheduled pages trigger"
  logic_app_id = azurerm_logic_app_workflow.logic_app_workflow.key_vault_id
  interval = 15
  frequency = "Minute"
}