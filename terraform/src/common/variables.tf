# ======================================================================================
# General Variables
# ======================================================================================
variable "resource_group" {
  description = "dct-crccms resource group"
}

variable "environment" {
  description = "Full environment name for tagging purpose."

  validation {
    condition     = contains(["development", "integration", "staging", "production"], var.environment)
    error_message = "Valid values for env are (development, integration, staging or production)"
  }
}

variable "env" {
  description = "Short environment name for resource names."

  validation {
    condition     = contains(["dev", "int", "stag", "prod"], var.env)
    error_message = "Valid values for env are (dev, int, stag or prod)"
  }
}

variable "location" {
  description = "Azure region where the resources will be created."

  validation {
    condition     = contains(["uks", "ukw"], var.location)
    error_message = "Valid values for location are (uks or ukw)"
  }
}

variable "long_location" {
  description = "Azure region where the resources will be created."

  validation {
    condition     = contains(["uksouth", "ukwest"], var.long_location)
    error_message = "Valid values for location are (uksouth or ukwest)"
  }
}

variable "deploy_container_apps" {
  type    = bool
  default = false
}

variable "username" {
  type        = string
  description = "Optional username for basic authentication"
  default     = null
}

variable "sha_512_password" {
  type        = string
  description = "Optional SHA-512 hash of password for basic authentication"
  default     = null
}

variable "crc_cms_version" {
  type        = string
  description = "The CRC CMS container image tag to deploy"
  default     = "latest"
}

variable "network_address_space" {
  type        = string
  description = "CIDR range for the spoke network"

  validation {
    condition     = can(cidrhost(var.network_address_space, 0))
    error_message = "Must be valid IPv4 CIDR."
  }
}

variable "aks_origin" {
  type = object({
    firewall_ip_address = string
    origin_host_header  = string
  })
  description = "Optional AKS origin on the Front Door origin group to allow for migration"
  default     = null
}

variable "imported_storage_subscription_id" {
  type        = string
  description = "subscription id for imported storage account"
}

variable "imported_storage_resource_group" {
  type        = string
  description = "original resource group for imported storage account"
}

variable "imported_storage_name" {
  type        = string
  description = "name of imported storage account"
}

