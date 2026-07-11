terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "techmart_bucket" {
  bucket = "techmart-pipeline-usama-2024"

  tags = {
    Name        = "TechMart Pipeline Bucket"
    Environment = "Dev"
    Project     = "TechMart"
  }
}

resource "aws_s3_bucket_versioning" "techmart_versioning" {
  bucket = aws_s3_bucket.techmart_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}