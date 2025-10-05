# ingestion/consumer/main.py
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "logs")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "log-analyzer")

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        group_id=CONSUMER_GROUP,
        auto_offset_reset='earliest'
    )
    print(f"Listening to Kafka topic: {KAFKA_TOPIC}")
    for message in consumer:
        print(f"Consumed message: {message.value.decode('utf-8')}")

if __name__ == "__main__":
    main()
