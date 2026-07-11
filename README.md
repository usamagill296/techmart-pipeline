# TechMart Real-Time Data Pipeline

A production-grade, end-to-end data engineering pipeline built for a fictional e-commerce platform called TechMart. This project demonstrates real-time data streaming, ETL processing, cloud storage, and infrastructure automation using industry-standard tools.

---

## Architecture

```
Fake Order Generator (Faker)
          ↓
    Apache Kafka
  (Real-time streaming)
          ↓
  Python ETL Consumer
  (pandas transformation)
          ↓
     AWS S3 Bucket
  (Cloud data storage)
          ↓
    [Coming soon]
  AWS Glue → Athena → Redshift
```

---

## Tech Stack

| Category | Tools |
|---|---|
| **Programming** | Python, SQL |
| **Streaming** | Apache Kafka, Zookeeper |
| **Data Processing** | pandas, Python ETL |
| **Cloud Storage** | AWS S3 |
| **Infrastructure** | Terraform (IaC) |
| **Containerization** | Docker, Docker Compose |
| **Version Control** | Git, GitHub |
| **Libraries** | kafka-python, boto3, faker, sqlalchemy |

---

## Project Structure

```
techmart-pipeline/
├── src/
│   ├── producer.py        # Generates fake orders → sends to Kafka
│   └── consumer.py        # Reads from Kafka → transforms → uploads to S3
├── config/
│   └── config.py          # Centralized configuration settings
├── terraform/
│   ├── main.tf            # AWS S3 bucket infrastructure
│   └── .terraform.lock.hcl
├── docker-compose.yml     # Kafka + Zookeeper setup
├── requirements.txt       # Python dependencies
└── .gitignore
```

---

## Features

- **Real-time streaming** — Orders flow through Kafka the moment they are generated
- **ETL processing** — pandas cleans, transforms and categorizes every order
- **Cloud storage** — Processed data automatically uploaded to AWS S3
- **Infrastructure as Code** — All AWS resources provisioned with Terraform
- **Containerized** — Kafka runs in Docker for consistent environments
- **Batch processing** — Orders processed in configurable batches

---

## Prerequisites

- Python 3.11+
- Docker Desktop
- AWS CLI configured with IAM credentials
- Terraform installed

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/usamagill296/techmart-pipeline.git
cd techmart-pipeline
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Kafka with Docker

```bash
docker-compose up -d
```

### 4. Provision AWS infrastructure with Terraform

```bash
cd terraform
terraform init
terraform apply
cd ..
```

### 5. Run the pipeline

Open two terminals:

**Terminal 1 — Start Producer:**
```bash
python src/producer.py
```

**Terminal 2 — Start Consumer:**
```bash
python src/consumer.py
```

---

## How It Works

### Producer (`src/producer.py`)
- Uses the `Faker` library to generate realistic fake e-commerce orders
- Each order contains customer name, email, city, product, quantity, and total amount
- Sends orders to Kafka topic `techmart-orders` every 2 seconds

### Consumer (`src/consumer.py`)
- Reads orders from Kafka topic in real time
- Uses `pandas` to transform and clean the data:
  - Converts dates to proper datetime format
  - Capitalizes customer names
  - Calculates revenue
  - Categorizes orders as Small / Medium / Large
- Saves processed batch to local CSV
- Uploads CSV to AWS S3 automatically using `boto3`

### Infrastructure (`terraform/main.tf`)
- Provisions AWS S3 bucket with versioning enabled
- Uses Terraform for repeatable, version-controlled infrastructure

---

## Sample Output

```
Starting TechMart Order Consumer...
Reading from Kafka topic: techmart-orders
--------------------------------------------------
Received: John Smith bought Laptop Pro for €999.99
Received: Anna Schmidt bought Python Book for €49.99
Received: Sara Khan bought Wireless Mouse for €59.98

==================================================
BATCH 1 SUMMARY
==================================================
Total Orders:  10
Total Revenue: €2,847.23
Average Order: €284.72
==================================================

Saved batch 1 to data/orders_batch_1.csv
✅ Uploaded to S3: s3://techmart-pipeline-usama-2024/processed/orders_batch_1.csv
```

---

## Roadmap

- [x] Kafka real-time streaming
- [x] Python ETL with pandas
- [x] AWS S3 storage with Terraform
- [ ] AWS Glue data catalog
- [ ] AWS Athena SQL querying
- [ ] AWS Redshift data warehouse
- [ ] Apache Airflow scheduling
- [ ] Apache Spark processing
- [ ] Docker containerization of pipeline
- [ ] GitHub Actions CI/CD

---

## Author

**Muhammad Usama** — Data Engineer
- GitHub: [github.com/usamagill296](https://github.com/usamagill296)
- Email: usamagill296@gmail.com
- Open to Data Engineer roles across Europe

---

## License

MIT License — feel free to use this project as a reference.
