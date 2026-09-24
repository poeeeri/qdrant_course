from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import numpy as np 

client = QdrantClient(
    url="http://localhost:6333",
    api_key="api_key",
    trust_env=False,
    check_compatibility=False,
)


# PointStruct - это связка айди вектора и метаданных о точке, чтобы удобно хранить ее в бд,
# а не полагаться на то, что сервер сам догадается, где у вашего словаря id, а где вектор
point1 = PointStruct(
    id=1,
    vector=np.random.normal(loc=0.0, scale=1.0, size=384).tolist(),
    payload={
        "title": "hello world",
        "category": "programming",
        "year": 2026
    }
)

point2 = PointStruct(
    id=2,
    vector=np.random.normal(loc=0.0, scale=1.0, size=384).tolist(),
    payload={
        "title": "введение в RAG",
        "category": "AI",
        "year": 2026
    }
)

client.upsert(
    collection_name="first_collection",
    points=[
        point1, point2
    ]
)

# Если вы загружаете сотни тысяч или миллионы точек, батчинг - это не оптимизация 
# "для продвинутых", а необходимость: разница между загрузкой по одной точке и батчами 
# по 256 может составлять кратные величины по времени, просто из-за накладных расходов
# на каждый отдельный сетевой запрос (TCP-соединение, сериализация, ожидание ответа).

BATCH = 2
all_points = [point1, point2]
for i in range(0, len(all_points), BATCH):
    client.upsert(
        collection_name="first_collection",
        points=all_points[i:i + BATCH],
    )