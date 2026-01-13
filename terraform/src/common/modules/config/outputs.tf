output "campaigns_monitoring_email" {
  value       = data.azurerm_key_vault_secret.budget_alert_email.value
  description = "Email address for the appropriate environment's campaigns monitoring slack channel"
}
