output "campaigns_monitoring_email" {
  value       = data.azurerm_key_vault_secret.campaigns_monitoring_email.value
  description = "Email address for the appropriate environment's campaigns monitoring slack channel"
}
output "nhsuk_infra_email" {
  value       = data.azurerm_key_vault_secret.nhsuk_infra_email.value
  description = "Email address for the NHS UK infrastructure team"
}
