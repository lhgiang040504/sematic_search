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
        })) -> dict[str, Any]:
    
    ingest_pipeline(request=req, connector_type=connector_type, config=config)
    return {
        "message": "Documents ingested successfully"
    }


@api.get("/search", tags=["Search"])
async def search_endpoint(
        request: Request, 
        strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
        query: str = Query(default="does human hair stop squirrels", description="MS MARCO Dataset: https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train"),
        max_results: int = 5,
        ) -> dict[str, Any]:
        
    search_results = search_pipeline(request, strategy_type, query, max_results)
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
