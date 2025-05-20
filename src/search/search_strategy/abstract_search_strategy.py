from abc import ABC, abstractmethod
from typing import List
from src.model import Passage, PassageResponse
from fastapi import Request


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, request: Request, query: str, max_results: int) -> List[Passage]:
        pass


def keyword_search(request: Request, query: str, max_results: int):
    # Connect to MongoDB
    database = request.app.mongodb.get_database()
    collection = database["documents"]

    # Assumes text index has been created on "content"
    collection.create_index([("content", "text")])
    cursor = collection.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(max_results)

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

