resource "azurerm_logic_app_action_http" "publish_scheduled_pages_request" {
  name         = "Publish scheduled pages request"
  logic_app_id = azurerm_logic_app_workflow.publish_scheduled_pages_workflow.id
  method       = "GET"
  uri          = var.publishing_endpoint
  headers      = { Authorization = "Bearer ${data.azurerm_key_vault_secret.pubToken.value}" }
  depends_on   = [azurerm_key_vault_access_policy.terraform_sp_access, azurerm_role_assignment.kv_reader]
}
