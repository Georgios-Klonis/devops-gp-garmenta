locals {
  env_code              = lower(var.environment)
  project_suffix_normal = "${local.env_code}-${var.project_suffix}"

  # GCP project configuration
  project_id   = "devops-garmenta-${local.project_suffix_normal}"
  project_name = "Devops Garmenta ${title(local.env_code)} ${var.project_suffix}"

}