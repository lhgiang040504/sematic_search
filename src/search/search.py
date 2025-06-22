from typing import Optional, Any
from prefect import flow
import logging

from src.model import SearchStrategyType
from src.search.search_strategy.search_strategy_factory import get_search_strategy_map
from fastapi import Request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

@flow(name="Search Pipeline")
def search_pipeline(strategy_type: SearchStrategyType, config: dict[str, Any]):
    logger.info(f"Starting search pipeline with strategy: {strategy_type}")
    # Get the search strategy based on the strategy type
    search_strategy = get_search_strategy_map().get(strategy_type)
    if not search_strategy:
        logger.error(f"Unknown search strategy type: {strategy_type}")
        raise ValueError(f"Unknown search strategy type: {strategy_type}")

    # Perform the search using the selected strategy
    search_results = search_strategy.search(config)
    logger.info(f"Search pipeline completed for strategy: {strategy_type}")
    return search_results

