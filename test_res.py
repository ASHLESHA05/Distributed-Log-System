from datetime import datetime
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

response = es.search(index="dummy_data", query={"match_all": {}})
print("Search Results:", response)