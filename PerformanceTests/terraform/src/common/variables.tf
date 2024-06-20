# ======================================================================================
# General Variables
# ======================================================================================
variable "resource_group" {
  description = "dct-testing resource group"
}

variable "load_testing_resource" {
  description = "CRCv3 load testing resource"
}

variable "environment" {
  description = "Full environment name for tagging purpose."
}

variable "tfstate_account_name" {
  description = "Terraform tfstate storage"
}

