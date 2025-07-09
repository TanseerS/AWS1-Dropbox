resource "aws_s3_bucket" "dropbox-bucket" {
  bucket = "dropbox-bucket"
  tags = {
    Name        = "dropbox-bucket"
    Environment = "Production"
  }
}