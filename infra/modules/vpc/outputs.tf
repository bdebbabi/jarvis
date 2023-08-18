output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnets_ids" {
  description = "The IDs of the private subnets of the VPC"
  value       = module.vpc.private_subnets
}