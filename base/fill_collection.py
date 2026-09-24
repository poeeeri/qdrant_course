from qdrant_client.models import PointStruct, Distance, VectorParams
from data.client_connect import client
from pathlib import Path
import json
import numpy as np


def take_from_file(file_path) -> list:
    with open(file_path, "r", encoding="utf-8") as documents:
        return json.load(documents)


def create_books_collection(client):
    try:
        client.create_collection(
            collection_name="books_collection",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    except:
        print("books_collection already exists!")
    return


def generate_point(item) -> PointStruct:
    return PointStruct(
        id=item["id"],
        vector=np.random.normal(loc=0.0, scale=1.0, size=384).tolist(),
        payload={
            "title": item["title"],
            "author":item["author"],
            "year": item["year"],
            "genre": item["genre"],
            "movement": item["movement"],
            "pages": item["pages"],
            "in_school_curriculum": item["in_school_curriculum"],
        }
    )


def main():
    file_path = Path("data/books_dataset.json")
    files = take_from_file(file_path)
    create_books_collection(client)
    points = []
    for f in files:
        points.append(generate_point(f))
    
    client.upsert(
        collection_name="books_collection",
        points=points
    )
    results = client.scroll(
        collection_name="books_collection",
        limit=100
    )
    print(results)


if __name__ == "__main__":
    main()