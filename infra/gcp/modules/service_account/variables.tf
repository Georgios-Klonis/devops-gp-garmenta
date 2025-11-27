variable "project_id" {
  description = "Project where the service account will live."
  type        = string
}

variable "account_id" {
  description = "Service account ID (without domain, e.g. terraform)."
  type        = string
}

variable "display_name" {
  description = "Display name for the service account."
  type        = string
  default     = null
}

variable "description" {
  description = "Optional description for the service account."
  type        = string
  default     = null
}

variable "roles" {
  description = "List of IAM roles to grant to the service account."
  type        = list(string)
  default     = []
}
