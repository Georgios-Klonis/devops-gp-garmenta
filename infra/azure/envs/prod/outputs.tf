# Bootstrap outputs
output "project_id" {
  description = "ID of the created dev project."
  value       = module.bootstrap.project_id
}

output "project_number" {
  description = "Numeric project identifier."
  value       = module.bootstrap.project_number
}