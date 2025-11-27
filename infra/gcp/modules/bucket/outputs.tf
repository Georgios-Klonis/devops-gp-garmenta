output "bucket_name" {
  description = "Name of the bucket."
  value       = google_storage_bucket.this.name
}

output "bucket_self_link" {
  description = "Self link of the bucket."
  value       = google_storage_bucket.this.self_link
}

output "bucket_url" {
  description = "URL of the bucket."
  value       = google_storage_bucket.this.url
}
