provider "google" {
  credentials = var.credentials_file != "" ? file(var.credentials_file) : null
  project     = local.project_id
}

provider "google-beta" {
  credentials = var.credentials_file != "" ? file(var.credentials_file) : null
  project     = local.project_id
}

module "bootstrap" {
  source          = "../../modules/bootstrap"
  project_id      = local.project_id
  project_name    = local.project_name
  org_id          = var.org_id
  folder_id       = var.folder_id
  billing_account = var.billing_account
  enabled_apis    = var.enabled_apis
}