provider "aws" {
  region = var.region
}

provider "aws" {
  alias  = "replica"
  region = "eu-west-1"
}

module "remote_state" {
  source = "nozaq/remote-state-s3-backend/aws"
  version = "1.5.0"

   providers = {
    aws         = aws
    aws.replica = aws.replica
  }

  override_s3_bucket_name = true
  s3_bucket_name = var.bucket
  enable_replication = false
  dynamodb_table_name = var.dynamodb_table
  dynamodb_enable_server_side_encryption = true
}
