variable "project_id" {
  description = "Project ID that will own the bucket."
  type        = string
}

variable "bucket_name" {
  description = "Globally unique name for the bucket."
  type        = string
}

variable "location" {
  description = "Bucket location/region (e.g. europe-west1)."
  type        = string
}

variable "storage_class" {
  description = "Storage class for the bucket."
  type        = string
  default     = "STANDARD"
}

variable "labels" {
  description = "Optional map of labels to apply to the bucket."
  type        = map(string)
  default     = {}
}

variable "uniform_bucket_level_access" {
  description = "Whether to enforce uniform bucket-level access."
  type        = bool
  default     = true
}

variable "versioning_enabled" {
  description = "Enable object versioning."
  type        = bool
  default     = false
}

variable "force_destroy" {
  description = "Force delete bucket even if it contains objects."
  type        = bool
  default     = false
}

variable "public_read" {
  description = "If true, grants allUsers roles/storage.objectViewer."
  type        = bool
  default     = false
}

variable "object_admin_members" {
  description = "Principals to grant roles/storage.objectAdmin."
  type        = list(string)
  default     = []
}

variable "object_writer_members" {
  description = "Principals to grant roles/storage.objectCreator."
  type        = list(string)
  default     = []
}

variable "object_reader_members" {
  description = "Principals to grant roles/storage.objectViewer."
  type        = list(string)
  default     = []
}
