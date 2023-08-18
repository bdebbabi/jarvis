resource "aws_iam_policy" "cert_manager_policy" {
  name        = "PolicyForCertManager"
  path        = "/"
  description = "Provides eks cert-manager with permission to validate Route 53 domain."

  policy = jsonencode({
    Version= "2012-10-17"
    Statement= [
        {
            Effect= "Allow"
            Action= "route53:GetChange"
            Resource= "arn:aws:route53:::change/*"
        },
        {
            Effect= "Allow"
            Action= [
                "route53:ChangeResourceRecordSets",
                "route53:ListResourceRecordSets"
            ],
            Resource= "arn:aws:route53:::hostedzone/${var.iam.route53_hosted_zone}"
        }
    ]
})
}

resource "aws_iam_role" "cert_manager_role" {
  name = "RoleForCertManager"
  description = "Provides eks cert-manager with role to validate Route 53 domain."

  assume_role_policy = jsonencode({
    Version= "2012-10-17"
    Statement= [
      {
        Effect= "Allow"
        Principal= {
          AWS= var.iam.eks_node_group_role
        },
        Action= "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "test-cert_manager_role_attachement" {
  role       = aws_iam_role.cert_manager_role.name
  policy_arn = aws_iam_policy.cert_manager_policy.arn
}