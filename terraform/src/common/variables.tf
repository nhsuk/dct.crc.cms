# ======================================================================================
# General Variables
# ======================================================================================
variable "resource_group" {
  description = "dct-crccms resource group"
}

variable "environment" {
  description = "Full environment name for tagging purpose."
}

variable "tfstate_account_name" {
  description = "Terraform tfstate storage"
}

variable "key_vault_rg" {
  description = "Key vault resource group"
}

variable "key_vault_name" {
  description = "Key vault name"
}

variable "publishing_endpoint" {
  description = "Endpoint for requesting publishing of scheduled pages"
}

# variable "campaigns_monitoring_webhook" {
#   description = "webhook url for campaigns monitoring slack channel"
# }

