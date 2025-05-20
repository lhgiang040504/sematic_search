from typing import Any, List
from fastapi import Request

from src.utils.hash import generate_md5_hash
from src.ingestion.chunking import semantic_chunk
from src.ingestion.connector.connector_main import get_connector_map
from src.model import Passage, ConnectorType
from src.ingestion.embedding import generate_embedding 

def ingest_pipeline(request: Request, connector_type: ConnectorType, config: dict[str, Any]):
    # Connect to data source
    connector_function = get_connector_map(config).get(connector_type)
    # Connect to database
    database = request.app.mongodb.get_database()
    collection = database["documents"]

    if not connector_function:
        raise Exception(f"No connector for: {connector_type}")

    for document in connector_function().load_data():
        cleaned_content = clean_document(document.content)
        semantic_passages = semantic_chunk(cleaned_content)
        for semantic_passage in semantic_passages:
            index_document(
                Passage(
                    **{
                        **document.model_dump(),
                        "content": semantic_passage,
                        "passage_id": generate_md5_hash(semantic_passage),
                        "embedding": generate_passage_embedding(semantic_passage)
                    }
                ),
                collection=collection,
            )

def clean_document(content: str) -> str:
    return content

def index_document(passage: Passage, collection) -> None:
    collection.update_one(
        {"passage_id": passage.passage_id},
        {"$set": passage.model_dump()},
        upsert=True
    )

def generate_passage_embedding(content: str) -> List[float]:
    return generate_embedding(content)