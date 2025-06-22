from abc import ABC, abstractmethod
from typing import List, Any
from prefect import task
import logging


from src.model import Passage, PassageResponse
from src.ingestion.embedding import generate_embedding
from src.utils.db_connection.mongodb_connector import get_collection
from fastapi import Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, config: dict[str, Any]) -> List[Passage]:
        pass

@task
def keyword_search(config: dict[str, Any]) -> List[Passage]:
    logger.info(f"Starting keyword search for query: {config.get('query', '')}")
    collection = get_collection(config['dataset_name'])
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
    logger.info(f"Keyword search completed for query: {query}")
    return to_passages(cursor)

@task
def vector_search(config: dict[str, Any]) -> List[Passage]:
    logger.info(f"Starting vector search for query: {config.get('query', '')}")
    collection = get_collection(config['dataset_name'])
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
    logger.info(f"Vector search completed for query: {query}")
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