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