from typing import Optional

from src.model import SearchStrategyType
from src.search.search_strategy.search_strategy_factory import get_search_strategy_map
from fastapi import Request


def search_pipeline(request: Request, strategy_type: SearchStrategyType, query: str, max_results: int):
    # Get the search strategy based on the strategy type
    search_strategy = get_search_strategy_map().get(strategy_type)
    if not search_strategy:
        raise ValueError(f"Unknown search strategy type: {strategy_type}")

    # Perform the search using the selected strategy
    search_results = search_strategy.search(request, query, max_results)

    return search_results

