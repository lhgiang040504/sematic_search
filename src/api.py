from typing import Any, Optional
from fastapi import Body, APIRouter, Request, Query

from src.ingestion.ingest import ingest_pipeline
from src.search.search import search_pipeline
from src.model import ConnectorType, SearchStrategyType, Passage, PassageResponse

api = APIRouter(prefix="/api")

@api.post("/ingest")
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


@api.get("/search",)
async def search_endpoint(
        req: Request, 
        strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
        query: str = Query(default="does human hair stop squirrels", description="MS MARCO Dataset: https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train"),
        max_results: int = 5,
        ) -> dict[str, Any]:
        
    search_results = search_pipeline(req, strategy_type, query, max_results)
    return {
        "results": search_results,
        "total_results": len(search_results),
    }
