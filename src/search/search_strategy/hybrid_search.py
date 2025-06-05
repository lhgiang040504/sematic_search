from typing import List, Any
from fastapi import Request

from src.model import Passage
from src.utils.query_expansion import expand_query
from src.search.search_strategy.abstract_search_strategy import SearchStrategy, keyword_search, vector_search

class HybridSearch(SearchStrategy):
    def search(self, request: Request, config: dict[str, Any]) -> List[Passage]:
        expanded_query = expand_query(config['query'])
        print(f"Expanded Query: {expanded_query}")
        passages = vector_search(request, config)
        print(f"Vector Search Results: {len(passages)} passages found")
        return passages

