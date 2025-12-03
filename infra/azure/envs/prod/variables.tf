# Common variables for the dev environment
variable "environment" {
  type        = string
  description = "Short environment code (dev, stg, prod, …)."
}

variable "project_suffix" {
  type        = string
  description = "Numeric suffix to keep resource names unique."
}

# GCP provider configuration
variable "credentials_file" {
  description = "Path to the service account JSON used by Terraform (leave empty to use ADC)."
  type        = string
  default     = ""
}

# Optional GCP organization hierarchy
variable "org_id" {
  description = "Optional organization ID to own the project."
  type        = string
  default     = null
}

variable "folder_id" {
  description = "Optional folder ID where the project should live."
  type        = string
  default     = null
}

variable "billing_account" {
  description = "Billing account ID to associate with the project."
  type        = string
}

variable "enabled_apis" {
  description = "List of APIs to enable for the project (e.g. serviceusage.googleapis.com)."
  type        = list(string)
  default     = []
}