from typing import Optional, Any
from prefect import flow

from src.model import SearchStrategyType
from src.search.search_strategy.search_strategy_factory import get_search_strategy_map
from fastapi import Request

@flow(name="Search Pipeline")
def search_pipeline(strategy_type: SearchStrategyType, config: dict[str, Any]):
    # Get the search strategy based on the strategy type
    search_strategy = get_search_strategy_map().get(strategy_type)
    if not search_strategy:
        raise ValueError(f"Unknown search strategy type: {strategy_type}")

    # Perform the search using the selected strategy
    search_results = search_strategy.search(config)

    return search_results

