from qdrant_client import QdrantClient
import os
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    # url=os.getenv("QDRANT_URL"),
    # api_key=os.getenv("QDRANT_API_KEY"), # не сработало
    check_compatibility=False,
    url="http://localhost:6333", 
    trust_env=False, 
    api_key="api_key")

try:
    client.create_collection(
        collection_name="first_collection",
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
except:
    print("error: first_collection already exists!")

client.create_collection(
    collection_name="named_collections",
    vectors_config={
        "title": VectorParams(size=384, distance=Distance.COSINE),
        "body": VectorParams(size=768, distance=Distance.COSINE)
})