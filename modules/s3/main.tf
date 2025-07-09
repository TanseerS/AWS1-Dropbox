# S3 Bucket Configuration
resource "aws_s3_bucket" "dropbox-bucket" {
  bucket = var.bucket-name
  tags = {
    Name        = var.bucket-name
    Environment = "Production"
  }
}

# Public Access Block Configuration
resource "aws_s3_bucket_public_access_block" "dropbox-public-access-block" {
  bucket = aws_s3_bucket.dropbox-bucket.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

# Bucket Versioning Configuration
resource "aws_s3_bucket_versioning" "dropbox-versioning" {
  bucket = aws_s3_bucket.dropbox-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Bucket encryption Configuration
resource "aws_s3_bucket_server_side_encryption_configuration" "dropbox-encryption" {
  bucket = aws_s3_bucket.dropbox-bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}