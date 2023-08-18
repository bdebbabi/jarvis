variable "iam" {
  type = object({
    route53_hosted_zone = string
    eks_node_group_role = string
  })
}