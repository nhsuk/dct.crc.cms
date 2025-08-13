variable "name" {
  description = "The name of the primary server."
  type        = string
}

variable "environment" {
  type        = string
  description = "The environment (development, integration, staging or production)."

  validation {
    condition     = contains(["development", "integration", "staging", "production"], var.environment)
    error_message = "Valid values for env are (development, integration, staging or production)"
  }
}

variable "resource_group" {
  description = "Azure resource group where primary resources will be deployed to."
  type = object({
    id       = string
    name     = string
    location = string
  })
}

variable "key_vault" {
  description = "Azure key vault to hold database credentials."
  type = object({
    id = string
  })
}

variable "log_analytics_workspace_id" {
  description = "ID of Log Analytics Workspace to send audit logs to"
  type        = string
}

variable "location" {
  description = "Azure region where the resources will be created."

  validation {
    condition     = contains(["uks", "ukw"], var.location)
    error_message = "Valid values for location are (uks or ukw)"
  }
}
