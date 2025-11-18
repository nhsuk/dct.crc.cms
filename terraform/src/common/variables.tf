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

variable "storage" {
  type = object({
    account   = string
    container = string
  })
  description = "The storage account and container names for hosting CRC content"
  default     = null
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

variable "dr_deployed" {
  type        = bool
  description = "Optional flag in primary region to say there is a DR site that should be added to the front door"
  default     = false
}

variable "container_resources" {
  description = "Container resource management/scaling configuration"
  type = object({
    haproxy = object({
      cpu                 = number
      memory              = string
      min_replicas        = number
      max_replicas        = number
      concurrent_requests = number
    }),
    redis = object({
      cpu                 = number
      memory              = string
      min_replicas        = number
      max_replicas        = number
      concurrent_requests = number
    }),
    wagtail = object({
      cpu                 = number
      memory              = string
      min_replicas        = number
      max_replicas        = number
      concurrent_requests = number
    })
  })
}
