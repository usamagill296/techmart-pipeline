import json
import pandas as pd
from kafka import KafkaConsumer
import boto3
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, BATCH_SIZE, AWS_BUCKET_NAME, AWS_REGION

def create_consumer():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    return consumer

def transform_orders(orders):
    df = pd.DataFrame(orders)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['processed_at'] = datetime.now().isoformat()
    df['customer_name'] = df['customer_name'].str.title()
    df['revenue'] = df['total_amount']
    df['order_size'] = df['total_amount'].apply(
        lambda x: 'Large' if x > 500 else ('Medium' if x > 100 else 'Small')
    )
    return df

def save_to_csv(df, batch_number):
    os.makedirs('data', exist_ok=True)
    filename = f"data/orders_batch_{batch_number}.csv"
    df.to_csv(filename, index=False)
    print(f"Saved batch {batch_number} to {filename}")
    return filename

def upload_to_s3(filename, batch_number):
    try:
        s3 = boto3.client('s3', region_name=AWS_REGION)
        s3_key = f"processed/orders_batch_{batch_number}.csv"
        s3.upload_file(filename, AWS_BUCKET_NAME, s3_key)
        print(f"Uploaded to S3: s3://{AWS_BUCKET_NAME}/{s3_key}")
    except Exception as e:
        print(f"S3 upload failed: {e}")

def print_summary(df, batch_number):
    print(f"\n{'='*50}")
    print(f"BATCH {batch_number} SUMMARY")
    print(f"{'='*50}")
    print(f"Total Orders:  {len(df)}")
    print(f"Total Revenue: €{df['revenue'].sum():.2f}")
    print(f"Average Order: €{df['revenue'].mean():.2f}")
    print(f"{'='*50}\n")

def run_consumer():
    print("Starting TechMart Order Consumer...")
    print(f"Reading from Kafka topic: {KAFKA_TOPIC}")
    print("-" * 50)

    consumer = create_consumer()
    orders_batch = []
    batch_number = 1

    for message in consumer:
        order = message.value
        orders_batch.append(order)
        print(f"Received: {order['customer_name']} bought "
              f"{order['product_name']} for €{order['total_amount']}")

        if len(orders_batch) >= BATCH_SIZE:
            print(f"\nProcessing batch {batch_number}...")
            df = transform_orders(orders_batch)
            print_summary(df, batch_number)
            filename = save_to_csv(df, batch_number)
            upload_to_s3(filename, batch_number)
            orders_batch = []
            batch_number += 1

if __name__ == "__main__":
    run_consumer()