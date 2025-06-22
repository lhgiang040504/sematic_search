from typing import Any, Optional
from fastapi import Body, APIRouter, Request, Query
import logging
import os

from src.ingestion.ingest import ingest_pipeline
from src.search.search import search_pipeline
from src.chat.chatbot import chat_pipeline
from src.model import ConnectorType, SearchStrategyType, Passage, PassageResponse, ChatRequest
from src.evaluation.metrics import precision_at_k, recall_at_k, average_precision, mean_average_precision, load_cranfield_ground_truth

api = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

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
    logger.info(f"Ingest endpoint called with connector_type: {connector_type}")
    ingest_pipeline(request=req, connector_type=connector_type, config=config)
    logger.info("Documents ingested successfully")
    return {
        "message": "Documents ingested successfully"
    }


@api.post("/search", tags=["Search"])
async def search_endpoint(
        request: Request, 
        strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
        config: dict = Body(default={
            "query": "feeding our back yard squirrels for the fall and winter",
            "dataset_name": "HuggingFaceDataset-v1.1-test",
            "max_results": 5
        })) -> dict[str, Any]:
    logger.info(f"Search endpoint called with strategy_type: {strategy_type}")
    search_results = search_pipeline(strategy_type, config)
    logger.info(f"Search completed with {len(search_results)} results")
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
    logger.info(f"Chat endpoint called with strategy_type: {strategy_type} and session_id: {chat_input.session_id}")
    config = {
        "query": chat_input.message,
        "dataset_name": "HuggingFaceDataset-v1.1-test",
        "max_results": max_results,
    }
    response_text = chat_pipeline(request, strategy_type, config)
    logger.info("Chat response generated")
    return {
        "response": response_text,
        "session_id": chat_input.session_id
    }

@api.post("/evaluate", tags=["Evaluation"])
async def evaluate_endpoint(
    request: Request,
    query_id: int = Body(..., embed=True),
    dataset_name: str = Body("Cranfield", embed=True),
    k: int = Body(10, embed=True),
    strategy_type: SearchStrategyType = SearchStrategyType.HYBRID_SEARCH,
    max_results: int = 20,
) -> dict[str, Any]:
    """
    Evaluate search results for a given query_id using IR metrics.
    """
    # 1. Load query text
    query_file = os.path.join("data", dataset_name, "TEST", "query.txt")
    with open(query_file, "r", encoding="utf-8") as f:
        query_lines = f.readlines()
    query_text = None
    for line in query_lines:
        if line.startswith(f"{query_id}\t") or line.startswith(f"{query_id} "):
            query_text = line.strip().split(None, 1)[-1]
            break
    if not query_text:
        return {"error": f"Query id {query_id} not found in {query_file}"}

    # 2. Run search
    config = {
        "query": query_text,
        "dataset_name": dataset_name,
        "max_results": max_results
    }
    search_results = search_pipeline(strategy_type, config)
    retrieved_doc_ids = [r.doc_id for r in search_results if hasattr(r, 'doc_id') and r.doc_id]

    # 3. Load ground truth
    res_dir = os.path.join("data", dataset_name, "TEST", "RES")
    relevant_doc_ids = load_cranfield_ground_truth(query_id, res_dir)

    # 4. Compute metrics
    # retrieved doc id like cranfield0486, but i only want to get the string valid number

    retrieved_doc_ids = [str(int(doc_id[9:])) for doc_id in retrieved_doc_ids]
    p_at_k = precision_at_k(retrieved_doc_ids, relevant_doc_ids, k)
    r_at_k = recall_at_k(retrieved_doc_ids, relevant_doc_ids, k)
    ap = average_precision(retrieved_doc_ids, relevant_doc_ids)
    # For MAP, just use this single query (for batch, would aggregate)
    map_score = mean_average_precision([retrieved_doc_ids], [relevant_doc_ids])

    return {
        "query_id": query_id,
        "query": query_text,
        "P@k": p_at_k,
        "R@k": r_at_k,
        "AP": ap,
        "MAP": map_score,
        "k": k,
        "retrieved_doc_ids": retrieved_doc_ids,
        "relevant_doc_ids": list(relevant_doc_ids),
        "total_relevant": len(relevant_doc_ids),
        "total_retrieved": len(retrieved_doc_ids),
    }