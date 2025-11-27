locals {
  normalized_object_admin_members = [
    for member in var.object_admin_members :
    can(regex(":", member)) ? member : "serviceAccount:${member}"
  ]

  normalized_object_writer_members = [
    for member in var.object_writer_members :
    can(regex(":", member)) ? member : "serviceAccount:${member}"
  ]

  normalized_object_reader_members = [
    for member in var.object_reader_members :
    can(regex(":", member)) ? member : "serviceAccount:${member}"
  ]
}

resource "google_storage_bucket" "this" {
  name                        = var.bucket_name
  project                     = var.project_id
  location                    = var.location
  storage_class               = var.storage_class
  labels                      = var.labels
  uniform_bucket_level_access = var.uniform_bucket_level_access
  force_destroy               = var.force_destroy

  versioning {
    enabled = var.versioning_enabled
  }
}

resource "google_storage_bucket_iam_member" "public_read" {
  count  = var.public_read ? 1 : 0
  bucket = google_storage_bucket.this.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_storage_bucket_iam_member" "object_admins" {
  for_each = toset(local.normalized_object_admin_members)

  bucket = google_storage_bucket.this.name
  role   = "roles/storage.objectAdmin"
  member = each.value
}

resource "google_storage_bucket_iam_member" "object_writers" {
  for_each = toset(local.normalized_object_writer_members)

  bucket = google_storage_bucket.this.name
  role   = "roles/storage.objectCreator"
  member = each.value
}

resource "google_storage_bucket_iam_member" "object_readers" {
  for_each = toset(local.normalized_object_reader_members)

  bucket = google_storage_bucket.this.name
  role   = "roles/storage.objectViewer"
  member = each.value
}
