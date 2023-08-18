variable "vpc" {
  type = object({
    id = string
    private_subnets_ids = list(string)
  })
}

variable "eks" {
  type = object({
    cluster_name = string
    cluster_version = string
    eks_admin_role_name = string
    initial_node_group_name = string
  })
}

variable "region"  {
  type        = string
}
