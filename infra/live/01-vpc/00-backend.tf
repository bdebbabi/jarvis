terraform {
  required_version = "1.5.5"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">=5.0.0"
    }
  }
  backend "s3" {
    bucket         = ""
    key            = "vpc/terraform.tfstate"
    region         = ""
    encrypt        = "true"
    kms_key_id     = ""
    dynamodb_table = ""
  }
}