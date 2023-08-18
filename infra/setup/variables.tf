variable "region" {
  description = "The AWS region in which resources are set up."
  type        = string
  default     = "eu-west-3"
}

variable "bucket" {
  description = "The S3 bucket name to create"
  type        = string
}

variable "dynamodb_table" {
  description = "The dynamodb table name to create"
  type        = string
}
