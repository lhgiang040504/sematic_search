from typing import List, Any
from fastapi import Request
from prefect import task
import logging

from src.model import Passage
from src.search.search_strategy.abstract_search_strategy import SearchStrategy, keyword_search, vector_search
from src.search.search_strategy.evaluate_search_strategy import evaluate_search_quality

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class HybridSearch(SearchStrategy):
    @task
    def search(self, config: dict[str, Any]) -> List[Passage]:
        logger.info(f"HybridSearch started for query: {config.get('query', '')}")
        passages = keyword_search(config)
        fallback_needed, vectorfallback_reason = evaluate_search_quality(passages, 'keyword')
        logger.warning(f'vectorfallback_reason: {vectorfallback_reason}')
        if fallback_needed:
            logger.info("Falling back to vector search.")
            passages = vector_search(config)
            fallback_needed, keywordfallback_reason = evaluate_search_quality(passages, 'vector')
            logger.warning(f'keywordfallback_reason: {keywordfallback_reason}')
            if fallback_needed:
                logger.warning("Both keyword and vector search failed. Returning empty result.")
                return []
        logger.info(f"HybridSearch completed for query: {config.get('query', '')}")
        return passages

