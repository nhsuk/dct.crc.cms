# ======================================================================================
# General Variables
# ======================================================================================
variable "resource_group" {
  description = "dct-crccms resource group"
}

variable "environment_long_name" {
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

variable "publish_endpoint" {
  description = "Endpoint for requesting publishing of scheduled pages"
  default = "https://crc-v3-review-schedule.nhswebsite-dev.nhs.uk/crc-admin/pub"
}

# variable "campaigns_monitoring_webhook" {
#   description = "webhook url for campaigns monitoring slack channel"
# }

