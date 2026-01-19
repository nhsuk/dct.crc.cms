variable "env" {
  description = "Short environment name for resource names."

  validation {
    condition     = contains(["dev", "int", "stag", "prod"], var.env)
    error_message = "Valid values for env are (dev, int, stag or prod)"
  }
}