from qdrant_client.models import PointStruct, Distance, VectorParams
from data.client_connect import client

client.delete_collection(
    collection_name="books_collection"
)