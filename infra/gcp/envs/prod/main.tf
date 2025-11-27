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

module "terraform_sa" {
  source       = "../../modules/service_account"
  project_id   = local.project_id
  account_id   = var.terraform_sa_account_id
  display_name = var.terraform_sa_display_name
  roles        = var.terraform_sa_roles
}

module "github_sa" {
  source       = "../../modules/service_account"
  project_id   = local.project_id
  account_id   = var.github_sa_account_id
  display_name = var.github_sa_display_name
  roles        = var.github_sa_roles
}

module "runtime_cloud_run_service_sa" {
  source       = "../../modules/service_account"
  project_id   = local.project_id
  account_id   = var.runtime_cloud_run_service_sa_account_id
  display_name = var.runtime_cloud_run_service_sa_display_name
  roles        = var.runtime_cloud_run_service_sa_roles
}