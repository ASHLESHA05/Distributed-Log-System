from datetime import datetime
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

# Dummy data to send to Elasticsearch
dummy_data = {
    "timestamp": datetime.now().isoformat(),
    "username": "john_doe",
    "message": "User logged in successfully",
    "status": "success"
}
index_name = "dummy_data"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# Index the data
response = es.index(index="dummy_data", document=dummy_data)

print(f"Data indexed: {response['_id']}")
