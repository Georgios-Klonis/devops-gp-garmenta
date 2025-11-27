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

# Terraform service account module variables
terraform_sa_roles = [
  "roles/iam.serviceAccountAdmin",         # CRUD service accounts
  "roles/serviceusage.serviceUsageAdmin",  # enable/disable APIs
  "roles/iam.serviceAccountUser",          # attach SAs to resources
  "roles/resourcemanager.projectIamAdmin", # manage IAM bindings at project level
  "roles/viewer",                          # read existing resources
  "roles/storage.admin",                   # manage GCS buckets/objects
  "roles/firebase.admin",                  # manage Firebase resources
  "roles/appengine.appAdmin",              # manage App Engine (required for Firestore)
  "roles/appengine.appCreator",            # create App Engine (required for Firestore)
  "roles/artifactregistry.admin",          # manage Artifact Registry repositories and images
  "roles/iam.workloadIdentityPoolAdmin",   # manage Workload Identity Pools and Providers
  "roles/secretmanager.admin",             # manage Secret Manager secrets and versions
  "roles/pubsub.admin",                    # manage Pub/Sub resources
  "roles/compute.securityAdmin"            # manage Compute Engine security policies

]

# Github Actions service account module variables
github_sa_roles = [
  "roles/run.admin",                       # deploy to Cloud Run
  "roles/iam.serviceAccountUser",          # use the GitHub Actions service account
  "roles/iam.serviceAccountAdmin",         # create/update service accounts
  "roles/resourcemanager.projectIamAdmin", # manage project-level IAM bindings
  "roles/storage.objectAdmin",             # manage GCS buckets/objects
  "roles/cloudbuild.builds.editor",        # trigger Cloud Build builds
  "roles/logging.logWriter",               # write logs to Cloud Logging
  "roles/cloudconfig.admin",               # manage Firebase Remote Config
  "roles/artifactregistry.writer"         # manage Artifact Registry repositories and images
]

# Runtime Users service account module variables
runtime_cloud_run_service_sa_roles = [
  "roles/run.invoker",                   # call other Cloud Run services
  "roles/run.developer",                 # trigger/execute Cloud Run jobs
  "roles/secretmanager.secretAccessor",  # read secrets from Secret Manager
  "roles/logging.logWriter",             # push logs to Cloud Logging
  "roles/monitoring.metricWriter",       # publish runtime metrics
  "roles/storage.objectAdmin",           # read/write GCS buckets/objects
  "roles/firebaseauth.admin",            # mint custom auth tokens / manage users
  "roles/iam.serviceAccountTokenCreator" # impersonate other service accounts - used for pubsub push subscriptions
]