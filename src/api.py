from typing import Optional, Any

from fastapi import Body, APIRouter
from fastapi import Query

from src.ingest.ingest import ingest_pipeline

from src.model import ConnectorType

api = APIRouter(prefix="/api")

@api.post("/ingest")
def ingest_endpoint(        
        connector_type: ConnectorType,
        config: dict = Body(default={
            "dataset_path": "microsoft/ms_marco",
            "dataset_name": "v1.1",
            "split": "train",
            "max_size": 100,
            "chunk_size": 100,
        })) -> dict[str, Any]:
    ingest_pipeline(connector_type=connector_type, config=config)
    return {
        "message": "Documents ingested successfully"
    }

