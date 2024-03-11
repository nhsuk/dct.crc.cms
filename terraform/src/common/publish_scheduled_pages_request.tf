resource "azurerm_logic_app_action_http" "publish_scheduled_pages_request" {
  name         = "Publish scheduled pages request"
  logic_app_id = azurerm_logic_app_workflow.publish_scheduled_pages_workflow.id
  method       = "GET"
  uri          = var.publishing_endpoint
  headers      = { Authorization = data.azurerm_key_vault_secret.pubToken.value }
  depends_on   = [azurerm_key_vault_access_policy.terraform_sp_access]
  # run_after {
  #   action_name   = azurerm_logic_app_action_custom.publish_scheduled_pages_get_secret.name
  #   action_result = "Succeeded"
  # }
}
