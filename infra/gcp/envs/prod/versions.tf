terraform {
  required_version = ">= 1.5.0"

  backend "gcs" {
    bucket = "devops-garmenta-prod-001-tfstate-bucket"
    prefix = "state/app"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}
