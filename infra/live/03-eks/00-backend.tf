terraform {
  required_version = "1.5.5"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">=5.0.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.9.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14"
    }
  }
  backend "s3" {
    bucket         = ""
    key            = "eks/terraform.tfstate"
    region         = ""
    encrypt        = "true"
    kms_key_id     = ""
    dynamodb_table = ""
  }
}

data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = var.bucket
    key    = "vpc/terraform.tfstate"
    region = var.region
  }
}
