from datetime import datetime
from enum import Enum
from typing import List, Optional
#from uuid import UUID, uuid4

from pydantic import BaseModel, Field

class Document(BaseModel):
    doc_id: str # UUID = uuid4()
    content: str

class ConnectorType(Enum):
    HUGGINGFACE_DATASET = "HUGGINGFACE_DATASET"
    FILE = "FILE"
    SQL = "SQL"

class Passage(BaseModel):
    doc_id: str
    passage_id: str
    content: str
