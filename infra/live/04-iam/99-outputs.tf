output "cert_manager_iam_role_arn" {
  description = "The arn of the cert manager role."
  value       = module.cert_manager_role.cert_manager_role_arn
}