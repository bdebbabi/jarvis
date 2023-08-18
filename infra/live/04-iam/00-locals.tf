data "aws_route53_zone" "selected" {
  name         = var.route53_hosted_zone
  private_zone = false
}

locals {
    cert_manager_iam_role = {
        route53_hosted_zone = data.aws_route53_zone.selected.zone_id
        eks_node_group_role = data.terraform_remote_state.eks.outputs.eks_managed_node_groups_iam_role_arn
    }
}