# Bucket Name
output "bucket-name" {
  description = "The name of the S3 bucket"
  value       = aws_s3_bucket.dropbox-bucket.bucket  
}

# Bucket ID
output "bucket-id" {
  description = "The ID of the S3 bucket"
  value       = aws_s3_bucket.dropbox-bucket.id
}

# Bucket ARN
output "bucket-arn" {
  description = "The ARN of the S3 bucket"
  value       = aws_s3_bucket.dropbox-bucket.arn
}

# Bucket Domain Name
output "bucket-domain-name" {
  description = "The domain name of the S3 bucket"
  value       = aws_s3_bucket.dropbox-bucket.bucket_domain_name
}