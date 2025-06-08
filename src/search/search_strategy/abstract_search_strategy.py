from abc import ABC, abstractmethod
from typing import List, Any

from src.model import Passage, PassageResponse
from src.ingestion.embedding import generate_embedding

from fastapi import Request


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, request: Request, config: dict[str, Any]) -> List[Passage]:
        pass


def keyword_search(request: Request, config: dict[str, Any]) -> List[Passage]:
    # Connect to MongoDB
    database = request.app.mongodb.get_database()
    collection = database[config["dataset_name"]]
    query = config.get("query", "")
    max_results = config.get("max_results", 10)

    # Inverted Index
    collection.create_index([("content", "text")])
    cursor = collection.find(
    {"$text": {"$search": query}},
    {
        "doc_id": 1,
        "passage_id": 1,
        "content": 1,
        "score": {"$meta": "textScore"}
    }).sort([("score", {"$meta": "textScore"})]).limit(max_results)

    return to_passages(cursor)


def vector_search(request: Request, config: dict[str, Any]) -> List[Passage]:
    # Connect to MongoDB
    database = request.app.mongodb.get_database()
    collection = database[config["dataset_name"]]
    query = config.get("query", "")
    max_results = config.get("max_results", 10)

    # Query embedding
    query_embedding = generate_embedding(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,  
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