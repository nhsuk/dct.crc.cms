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

variable "postgresql_server" {
  description = "Name of the PostgreSQL server."
  type        = string
}

variable "postgresql_resource_group" {
  description = "The name of the resource group containing the PostgreSQL server"
  type        = string
}
