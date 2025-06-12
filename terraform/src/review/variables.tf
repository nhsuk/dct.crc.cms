variable "dev_instance" {
  type        = string
  description = "Name of the dev instance, for example pr-23 or new-feature"
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]*[a-z0-9]$", var.dev_instance))
    error_message = "var.dev_instance can only be used in dev environment and must be lowercase letters and numbers with dashes in the middle"
  }
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
}
