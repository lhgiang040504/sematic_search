from typing import Any

from src.model import ConnectorType
from src.ingestion.connector.huggingface_dataset_connector import HuggingFaceConnector

def get_connector_map(config: dict[str, Any]):
    return {
        ConnectorType.HUGGINGFACE_DATASET: lambda: HuggingFaceConnector(
            dataset_path=config["dataset_path"],
            dataset_name=config["dataset_name"],
            split=config["split"],
            max_size=config["max_size"],
            chunk_size=config["chunk_size"]
        )
    }