# Common environment identifiers
environment    = "prod"
project_suffix = "001"

# GCP provider configuration
# credentials_file = "./.secrets/terraform-sa.json"
credentials_file = ""

# Optional hierarchy overrides
org_id          = null
folder_id       = null
billing_account = "0191A9-5E15B6-620E72"
enabled_apis = [
  "cloudresourcemanager.googleapis.com",
  "serviceusage.googleapis.com",
  "iam.googleapis.com",
  "cloudbilling.googleapis.com",
  "firebase.googleapis.com",
  "firebaserules.googleapis.com",
  "firebasehosting.googleapis.com",
  "identitytoolkit.googleapis.com",
  "storage.googleapis.com",
  "appengine.googleapis.com",
  "run.googleapis.com",
  "servicemanagement.googleapis.com",
  "servicecontrol.googleapis.com",
  "cloudfunctions.googleapis.com",
  "cloudbuild.googleapis.com",
  "container.googleapis.com",
  "compute.googleapis.com",
  "artifactregistry.googleapis.com",
  "logging.googleapis.com",
  "secretmanager.googleapis.com",
]