from qdrant_client.models import PointStruct, Distance, VectorParams
from data.client_connect import client
from pathlib import Path
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os


load_dotenv()
model_path = Path(os.getenv("MODEL_PATH"))
model = SentenceTransformer(str(model_path))


def take_from_file(file_path) -> list:
    with open(file_path, "r", encoding="utf-8") as documents:
        return json.load(documents)


def create_books_collection(client):
    try:
        client.create_collection(
            collection_name="books_collection",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        return True
    except:
        print("books_collection already exists!")
        return False


def generate_point(item) -> PointStruct:
    return PointStruct(
        id=item["id"],
        vector=model.encode(item["text"]),
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
    if not create_books_collection(client):
        points = []
        for f in files:
            points.append(generate_point(f))
    
        client.upsert(
            collection_name="books_collection",
            points=points
        )

    hits = client.query_points(
        collection_name="books_collection",
        query=model.encode("золотая рыба исполняет желания"),
        limit=3,
    ).points
    # 85 0.645 На дне
    # 25 0.598 Вий
    # 4 0.577 Обломов
    print([print(hit.id, round(hit.score, 3), hit.payload.get("title")) for hit in hits])


if __name__ == "__main__":
    main()