from typing import Any, List

from prefect import flow
from prefect import task

from src.utils.elasticsearch import get_elasticsearch_client
from src.utils.hash import generate_md5_hash
from src.ingest.chunking import semantic_chunk
from src.ingest.connector.connector_main import get_connector_map
from src.ingest.embedding import generate_embedding
from src.model import Passage, ConnectorType


@flow
def ingest_pipeline(connector_type: ConnectorType, config: dict[str, Any]):
    connector_function = get_connector_map(config).get(connector_type)

    if not connector_function:
        raise Exception(f"No connector for: {connector_type}")

    setup_passage_index()
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
                )
            )


@task
def clean_document(content: str) -> str:
    return content


@task()
def setup_passage_index():
    es = get_elasticsearch_client()
    if not es.indices.exists(index=PASSAGE_INDEX):
        es.indices.create(
            index=PASSAGE_INDEX,
            body=PASSAGE_INDEX_SETTINGS,
        )


@task
def index_document(passage: Passage) -> None:
    es = get_elasticsearch_client()
    es.index(
        index=PASSAGE_INDEX,
        id=passage.passage_id,
        document=passage.model_dump()
    )


@task
def generate_passage_embedding(content: str) -> List[float]:
    return generate_embedding(content)


def create_elasticsearch_index(index_name: str, index_settings: dict[str, Any]):
    es = get_elasticsearch_client()
    if not es.indices.exists(index=index_name):
        es.indices.create(
            index=index_name,
            body=index_settings
        )


PASSAGE_INDEX = "passages"

PASSAGE_INDEX_SETTINGS = {
    "mappings": {
        "properties": {
            "doc_id": {
                "type": "keyword"
            },
            "passage_id": {
                "type": "keyword"
            },
            "content": {
                "type": "text"
            },
            "created_at": {
                "type": "date"
            },
            "updated_at": {
                "type": "date"
            },
            "effective_at": {
                "type": "date"
            },
            "expired_at": {
                "type": "date"
            },
            "embedding": {
                "type": "dense_vector",
                "dims": 768,
                "similarity": "cosine"
            }
        }
    }
}