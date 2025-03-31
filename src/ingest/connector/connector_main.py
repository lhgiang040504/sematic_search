from typing import Any

from src.model import ConnectorType
from src.ingest.connector.file_connector import FileConnector
from src.ingest.connector.huggingface_dataset_connector import HuggingFaceConnector
from src.ingest.connector.sql_connector import SQLConnector

def get_connector_map(config: dict[str, Any]):
    return {
        ConnectorType.HUGGINGFACE_DATASET: lambda: HuggingFaceConnector(
            dataset_path=config["dataset_path"],
            dataset_name=config["dataset_name"],
            split=config["split"],
            max_size=config["max_size"],
            chunk_size=config["chunk_size"]
        ),
        ConnectorType.FILE: lambda: FileConnector(
            file_paths=config["file_paths"],
        ),
        ConnectorType.SQL: lambda: SQLConnector(
            connection_string=config["connection_string"],
            query=config["query"],
        )
    }