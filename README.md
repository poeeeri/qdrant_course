Установите через терминал клиента:
```
pip install qdrant-client
```

код подключения к Qdrant Cloud:
```from qdrant_client import QdrantClient
client = QdrantClient(
    url="https://xxxxx-xxxx.aws.cloud.qdrant.io",
    api_key="ВАШ_API_КЛЮЧ",
)
print(client.get_collections())```