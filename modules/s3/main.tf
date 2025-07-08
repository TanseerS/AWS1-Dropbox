resource "aws_s3_bucket" "dropbox-bucket" {
  bucket = "dropbox-bucket"
  tags = {
    Name        = "dropbox-bucket"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_ownership_controls" "ownership" {
    bucket = aws_s3_bucket.dropbox-bucket.id
    rule {
        object_ownership = "BucketOwnerPreferred"
    }
}