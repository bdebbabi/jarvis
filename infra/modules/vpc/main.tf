module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.1"

  name = var.vpc.name
  cidr = var.vpc.vpc_cidr

  azs             = var.vpc.azs
  public_subnets  = var.vpc.public_subnet_cidrs
  private_subnets = var.vpc.private_subnet_cidrs

  enable_nat_gateway   = true
  create_igw           = true
  enable_dns_hostnames = true
  single_nat_gateway   = true

  manage_default_network_acl    = true
  default_network_acl_tags      = { Name = "${var.vpc.name}-default" }
  manage_default_route_table    = true
  default_route_table_tags      = { Name = "${var.vpc.name}-default" }
  manage_default_security_group = true
  default_security_group_tags   = { Name = "${var.vpc.name}-default" }

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }

}
