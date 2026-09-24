from base.qdrant_point_struct import client
from qdrant_client.models import Filter, FieldCondition, MatchValue

result = client.retrieve(
    collection_name="first_collection",
    ids=[1,2],
    with_vectors=True
)

# print(result)

# scroll- когда нужно пройтись по всей коллекции целиком: выгрузка данных, 
# миграция, пересчёт эмбеддингов после смены модели. Не пытайтесь выгрузить 
# всё одним вызовом через огромный limit - это курсорная пагинация именно для 
# того, чтобы не держать миллионы точек в памяти одновременно

points, next_offset = client.scroll(
    collection_name="first_collection",
    limit=100,
    with_payload=True,
    with_vectors=False
)


# избавляет от проблемы с upsert
client.set_payload(
    collection_name="first_collection",
    payload={"year": 1999},
    points=[1]
)


point1 = client.retrieve(
    collection_name="first_collection",
    ids=[1],
)
print(point1)


client.delete_payload(
    collection_name="first_collection",
    keys=["year"],
    points=[1]
)



point1 = client.retrieve(
    collection_name="first_collection",
    ids=[1],
)
print(point1)


client.delete(

    collection_name="first_collection",
    points_selector=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="deprecated"))]
    ),
)