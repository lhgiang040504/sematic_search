from typing import Any, Optional
from fastapi import Body, APIRouter, Request, Query

from src.ingestion.ingest import ingest_pipeline
from src.search.search import search_pipeline
from src.chat.chatbot import chat_pipeline

from src.model import ConnectorType, SearchStrategyType, Passage, PassageResponse, ChatRequest

api = APIRouter(prefix="/api")

@api.post("/ingest", tags=["Ingestion"])
def ingest_endpoint( 
        req: Request,       
        connector_type: ConnectorType,
        config: dict = Body(default={
            "dataset_path": "microsoft/ms_marco",
            "dataset_name": "v1.1",
            "split": "test",
            "max_size": 100,
            "chunk_size": 100,
            "dataset_folderpath": "C:\\Users\\Lenovo\\learning\\sematic_search\\data\\Cranfield\\Cranfield"
        })) -> dict[str, Any]:
    
    ingest_pipeline(request=req, connector_type=connector_type, config=config)
    return {
        "message": "Documents ingested successfully"
    }


@api.post("/search", tags=["Search"])
async def search_endpoint(
        request: Request, 
        strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
        config: dict = Body(default={
            "query": "does human hair stop squirrels",
            "dataset_name": "HuggingFaceDataset-v1.1-test",
            "max_results": 5
        })) -> dict[str, Any]:
        
    search_results = search_pipeline(request, strategy_type, config)
    return {
        "results": search_results,
        "total_results": len(search_results),
    }


@api.post("/chat", tags=["Chatbot"])
async def chat_endpoint(
        request: Request,
        strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
        chat_input: ChatRequest = Body(default=ChatRequest(message="does human hair stop squirrels", session_id=None)),
        max_results: int = 5,
        ) -> dict[str, Any]:
    response_text = chat_pipeline(request, strategy_type, max_results, chat_input.message, chat_input.session_id)
    return {
        "response": response_text,
        "session_id": chat_input.session_id
    }
