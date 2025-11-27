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

# Terraform service account module variables
variable "terraform_sa_roles" {
  description = "List of IAM roles to grant to the Terraform service account."
  type        = list(string)
  default     = []
}

variable "terraform_sa_account_id" {
  description = "Service account ID for the Terraform service account."
  type        = string
  default     = "terraform"
}

variable "terraform_sa_display_name" {
  description = "Display name for the Terraform service account."
  type        = string
  default     = "Terraform Service Account"
}

# Github Actions service account module variables
variable "github_sa_roles" {
  description = "List of IAM roles to grant to the Github Actions service account."
  type        = list(string)
  default     = []
}

variable "github_sa_account_id" {
  description = "Service account ID for the GitHub Actions service account."
  type        = string
  default     = "github-actions"
}

variable "github_sa_display_name" {
  description = "Display name for the GitHub Actions service account."
  type        = string
  default     = "GitHub Actions Service Account"
}

# Runtime Cloud Run service account module variables
variable "runtime_cloud_run_service_sa_roles" {
  description = "List of IAM roles to grant to the Runtime Microservices service account."
  type        = list(string)
  default     = []
}

variable "runtime_cloud_run_service_sa_account_id" {
  description = "Service account ID for the runtime Cloud Run services."
  type        = string
  default     = "runtime-cloud-run-service"
}

variable "runtime_cloud_run_service_sa_display_name" {
  description = "Display name for the runtime Cloud Run services account."
  type        = string
  default     = "Runtime Cloud Run Service Account"
}