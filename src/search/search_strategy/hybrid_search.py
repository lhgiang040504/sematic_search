from typing import List
from fastapi import Request

from src.model import Passage
from src.utils.query_expansion import expand_query
from src.search.search_strategy.abstract_search_strategy  import SearchStrategy, keyword_search, vector_search


class HybridSearch(SearchStrategy):
    def search(self, request: Request, query: str, max_results: int) -> List[Passage]:
        expanded_query = expand_query(query)
        passages = vector_search(request, expanded_query, max_results)
        return passages

