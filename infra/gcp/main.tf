terraform {
  required_version = ">= 1.6"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}
variable "project_id" { type = string }
variable "bucket_name" { type = string }
variable "region" {
  type = string
  default = "europe-north1"
}
provider "google" { project = var.project_id }
resource "google_storage_bucket" "data" {
  name = var.bucket_name
  location = var.region
  force_destroy = false
  uniform_bucket_level_access = true
  public_access_prevention = "enforced"
}
