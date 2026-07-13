import json
import time
import random
from faker import Faker
from kafka import KafkaProducer
import sys
import os

# Add config folder to path so we can import it
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.config import KAFKA_TOPIC, SLEEP_SECONDS
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Initialize Faker — generates realistic fake data
fake = Faker()

# ── What products TechMart sells ─────────────
PRODUCTS = [
    {"name": "Laptop Pro", "category": "Electronics", "price": 999.99},
    {"name": "Wireless Mouse", "category": "Electronics", "price": 29.99},
    {"name": "Mechanical Keyboard", "category": "Electronics", "price": 79.99},
    {"name": "USB Hub", "category": "Electronics", "price": 39.99},
    {"name": "Python Book", "category": "Books", "price": 49.99},
    {"name": "Data Engineering Book", "category": "Books", "price": 59.99},
    {"name": "Standing Desk", "category": "Furniture", "price": 299.99},
    {"name": "Monitor 27inch", "category": "Electronics", "price": 349.99},
]

def generate_order():
    """
    Generate one fake TechMart order
    Returns a dictionary with order details
    """
    product = random.choice(PRODUCTS)
    quantity = random.randint(1, 5)

    order = {
        "order_id": fake.uuid4(),
        "customer_name": fake.name(),
        "customer_email": fake.email(),
        "customer_city": fake.city(),
        "product_name": product["name"],
        "category": product["category"],
        "price": product["price"],
        "quantity": quantity,
        "total_amount": round(product["price"] * quantity, 2),
        "order_date": fake.date_time_this_year().isoformat(),
        "status": "pending"
    }
    return order

def create_producer():
    """
    Connect to Kafka with retry logic
    """
    import time
    retries = 10
    for i in range(retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            print("Connected to Kafka successfully!")
            return producer
        except Exception as e:
            print(f"Kafka not ready yet... attempt {i+1}/{retries}. Waiting 10 seconds...")
            time.sleep(10)
    raise Exception("Could not connect to Kafka after multiple attempts")

def run_producer():
    print(f"Connecting to Kafka at: {KAFKA_BOOTSTRAP_SERVERS}")  # ADD THIS
    print("Starting TechMart Order Producer...")
    """
    Main function — generates orders and sends to Kafka
    """
    print("Starting TechMart Order Producer...")
    print(f"Sending orders to Kafka topic: {KAFKA_TOPIC}")
    print("-" * 50)

    producer = create_producer()
    order_count = 0

    while True:
        # Generate a fake order
        order = generate_order()

        # Send to Kafka
        producer.send(KAFKA_TOPIC, value=order)

        order_count += 1
        print(f"Order #{order_count} sent: {order['customer_name']} bought {order['product_name']} for €{order['total_amount']}")

        # Wait before sending next order
        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    run_producer()