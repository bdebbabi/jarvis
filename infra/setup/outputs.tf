output "kms_key_arn" {
  description = "The KMS customer master key arn to encrypt state buckets."
  value       = module.remote_state.kms_key.arn
}