# Outputs for the S3 bucket module
output "bucket_name" {
  description = "The name of the S3 bucket"
  value       = module.s3.bucket-name
}

output "bucket_id" {
  description = "The ID of the S3 bucket"
  value       = module.s3.bucket-id
}

output "bucket_arn" {
  description = "The ARN of the S3 bucket"
  value       = module.s3.bucket-arn
}

output "bucket_domain_name" {
  description = "The domain name of the S3 bucket"
  value       = module.s3.bucket-domain-name
}
