from enum import Enum
from typing import List, Optional
#from uuid import UUID, uuid4

from pydantic import BaseModel

class Document(BaseModel):
    doc_id: str # UUID = uuid4()
    content: str

class ConnectorType(Enum):
    HUGGINGFACE_DATASET = "HUGGINGFACE_DATASET"
    CRANFIELD = "CRANFIELD"

class Passage(BaseModel):
    doc_id: str
    passage_id: str
    content: str
    embedding: List[float]

class PassageResponse(BaseModel):
    doc_id: Optional[str]
    passage_id: Optional[str]
    content: str
    score: Optional[float] = None

class SearchStrategyType(Enum):
    HYBRID_SEARCH = "HYBRID_SEARCH"
    FALLBACK_MECHANISM = "FALLBACK_MECHANISM"
    TIERED_SEARCH = "TIERED_SEARCH"

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None  # Optional: if you want to support session-based chat
