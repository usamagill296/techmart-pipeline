# ── Kafka Settings ──────────────────────────
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'techmart-orders'

# ── AWS Settings ────────────────────────────
AWS_BUCKET_NAME = 'techmart-pipeline-usama-2024'
AWS_REGION = 'eu-central-1'

# ── Pipeline Settings ───────────────────────
BATCH_SIZE = 10        # process 10 orders at a time
SLEEP_SECONDS = 2      # wait 2 seconds between batches