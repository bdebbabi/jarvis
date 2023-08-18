data "aws_caller_identity" "current" {}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.4"

  cluster_name                   = var.eks.cluster_name
  cluster_version                = var.eks.cluster_version
  cluster_endpoint_public_access = true

  vpc_id     = var.vpc.id
  subnet_ids = var.vpc.private_subnets_ids

  #we uses only 1 security group to allow connection with Fargate, MNG, and Karpenter nodes
  create_node_security_group = false
  eks_managed_node_groups = {
    initial = {
      node_group_name = var.eks.initial_node_group_name
      instance_types  = ["t2.medium"]

      min_size     = 1
      max_size     = 3
      desired_size = 1
      subnet_ids   = var.vpc.private_subnets_ids
    }
  }

  manage_aws_auth_configmap = true
  aws_auth_roles = flatten([
    {
      rolearn  = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.eks.eks_admin_role_name}" # The ARN of the IAM role
      username = "ops-role"                                                                                      # The user name within Kubernetes to map to the IAM role
      groups   = ["system:masters"]                                                                              # A list of groups within Kubernetes to which the role is mapped; Checkout K8s Role and Rolebindings
    }
  ])
}

data "aws_eks_cluster" "default" {
  name = module.eks.cluster_name
  depends_on = [ module.eks.eks_managed_node_groups ]
}

data "aws_eks_cluster_auth" "default" {
  name = module.eks.cluster_name
  depends_on = [ module.eks.eks_managed_node_groups ]
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.default.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.default.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.default.token
}