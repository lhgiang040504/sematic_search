from abc import ABC, abstractmethod
from typing import List

from src.model import Passage, PassageResponse
from src.ingestion.embedding import generate_embedding

from fastapi import Request


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, request: Request, query: str, max_results: int) -> List[Passage]:
        pass


def keyword_search(request: Request, query: str, max_results: int):
    # Connect to MongoDB
    database = request.app.mongodb.get_database()
    collection = database["documents"]

    # Inverted Index
    collection.create_index([("content", "text")])
    cursor = collection.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(max_results)

    return to_passages(cursor)


def vector_search(request: Request, query: str, max_results: int) -> List[Passage]:
    # Connect to MongoDB
    database = request.app.mongodb.get_database()
    collection = database["documents"]

    # Query embedding
    query_embedding = generate_embedding(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",  # tên index bạn đã tạo
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,   # bạn có thể điều chỉnh
                "limit": max_results
            }
        },
        {
            "$project": {
                "_id": 0,
                "doc_id": 1,
                "passage_id": 1,
                "content": 1,
                "embedding": 1,
                "score": { "$meta": "vectorSearchScore" }
            }
        }
    ]

    # Run the aggregation pipeline
    cursor = collection.aggregate(pipeline)

    return to_passages(cursor)


def to_passages(cursor) -> List[PassageResponse]:
    passages = []
    for doc in cursor:
        passage = PassageResponse(
            doc_id=doc.get("doc_id", ""),
            passage_id=doc.get("passage_id", ""),
            content=doc.get("content", ""),
            score=doc.get("score", 0.0)  # Assuming score is a float
        )
        passages.append(passage)    
    return passages