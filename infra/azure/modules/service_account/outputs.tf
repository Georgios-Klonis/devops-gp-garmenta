output "service_account_email" {
  description = "Email of the created service account."
  value       = google_service_account.this.email
}

output "service_account_name" {
  description = "Resource name of the service account."
  value       = google_service_account.this.name
}
