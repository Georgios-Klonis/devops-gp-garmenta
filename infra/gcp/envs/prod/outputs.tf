# Bootstrap outputs
output "project_id" {
  description = "ID of the created dev project."
  value       = module.bootstrap.project_id
}

output "project_number" {
  description = "Numeric project identifier."
  value       = module.bootstrap.project_number
}

# Terraform service account outputs
output "terraform_service_account_email" {
  description = "Email of the Terraform service account."
  value       = module.terraform_sa.service_account_email
}

# Github Actions service account outputs
output "github_service_account_email" {
  description = "Email of the Github Actions service account."
  value       = module.github_sa.service_account_email
}

# Runtime Cloud Run service account outputs
output "runtime_cloud_run_service_service_account_email" {
  description = "Email of the Runtime Cloud Run service account."
  value       = module.runtime_cloud_run_service_sa.service_account_email
}