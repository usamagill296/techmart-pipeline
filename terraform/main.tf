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

# ── Glue Database ────────────────────────────
resource "aws_glue_catalog_database" "techmart_db" {
  name = "techmart_database"
}

# ── Glue IAM Role ────────────────────────────
resource "aws_iam_role" "glue_role" {
  name = "techmart-glue-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# ── Glue Crawler ─────────────────────────────
resource "aws_glue_crawler" "techmart_crawler" {
  database_name = aws_glue_catalog_database.techmart_db.name
  name          = "techmart-orders-crawler"
  role          = aws_iam_role.glue_role.arn

  s3_target {
    path = "s3://${aws_s3_bucket.techmart_bucket.bucket}/processed/"
  }

  schedule = "cron(0 * * * ? *)"

  tags = {
    Project = "TechMart"
  }
}