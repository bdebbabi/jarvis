module "ecr" {

  source = "terraform-aws-modules/ecr/aws"

  repository_name = var.ecr.name
  create_lifecycle_policy = false
  repository_force_delete = true
}