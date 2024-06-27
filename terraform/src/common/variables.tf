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

variable "location" {
  description = "Azure region where the resources will be created."
}