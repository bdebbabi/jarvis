variable "region"  {
  description = "AWS Region"
  type        = string
  default     = "eu-west-3"
}

variable "bucket"  {
  description = "AWS S3 remote state bucket"
  type        = string
}