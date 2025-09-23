terraform {
  backend "s3" {
    bucket         = "my-test-state-bucket-terraform"     
    key            = "dropbox/terraform.tfstate" 
    region         = "ap-south-1"                      
    encrypt        = true
  }
}
