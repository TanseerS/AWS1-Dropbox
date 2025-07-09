module "name" {
  source = "./modules/s3"
  bucket-name = var.bucket-name
}