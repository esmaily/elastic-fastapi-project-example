from elasticsearch import Elasticsearch
# from sentence_transformers import SentenceTransformer
from app.core.config import settings

# Connect to Elasticsearch
es = Elasticsearch(settings.ELASTIC_SEARCH_URL)

# Index name
index_name = "articles"

# Create Elasticsearch index and mapping
if not es.indices.exists(index=index_name):
    es_index = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
    }
    es.indices.create(index=index_name, body=es_index, ignore=[400])
