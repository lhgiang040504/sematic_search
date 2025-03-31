from datetime import datetime
from enum import Enum
from typing import List, Optional
#from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class Document(BaseModel):
    doc_id: str # UUID = uuid4()
    content: str
    created_at: datetime
    updated_at: datetime
    effective_at: datetime
    expired_at: datetime

class ConnectorType(Enum):
    HUGGINGFACE_DATASET = "HUGGINGFACE_DATASET"
    FILE = "FILE"
    SQL = "SQL"
    URL = "URL"

class Passage(BaseModel):
    doc_id: str
    passage_id: str
    content: str
    embedding: List[float]
