from typing import Any, List
from fastapi import Request
from prefect import flow
from prefect import task
import logging

from src.utils.hash import generate_md5_hash
from src.ingestion.chunking import semantic_chunk
from src.ingestion.connector.connector_main import get_connector_map
from src.model import Passage, ConnectorType
from src.ingestion.embedding import generate_embedding 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def ingest_pipeline(request: Request, connector_type: ConnectorType, config: dict[str, Any]):
    logger.info(f"Starting ingestion for connector: {connector_type}")
    # Connect to data source
    connector_function = get_connector_map(config).get(connector_type)
    # Connect to database
    database = request.app.mongodb.get_database()
    collection_name = connector_function().name if connector_function else None
    collection = database[collection_name] if collection_name else None

    if not connector_function:
        logger.error(f"No connector for: {connector_type}")
        raise Exception(f"No connector for: {connector_type}")

    for document in connector_function().load_data():
        cleaned_content = clean_document(document.content)
        semantic_passages = semantic_chunk(cleaned_content)
        doc_id = document.doc_id

        for id, semantic_passage in enumerate(semantic_passages):
            chunk_id = f'{doc_id}_{int(id):04d}'
                
            # Create document and store
            doc_to_store = Passage(
                **{
                    **document.model_dump(),
                    "content": semantic_passage,
                    "passage_id": f'{chunk_id}_{generate_md5_hash(semantic_passage)}',
                    "embedding": generate_passage_embedding(semantic_passage),
                }
            )
            index_document(doc_to_store, collection=collection)
    logger.info(f"Ingestion completed for connector: {connector_type}")

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