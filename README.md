# Dropbox-Style Serverless Storage with AWS and Terraform

This project is a **Dropbox-style** file storage system built with AWS serverless services and managed as code using Terraform.
The system allows users to securely upload files and retrieve them later, with core features including:
- Secure File Uploads via Presigned URLs
- Metadata Tracking with DynamoDB
- Notification via SNS
- CDN Delivery (CloudFront)