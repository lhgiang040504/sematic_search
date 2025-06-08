from typing import List, Any
from fastapi import Request

from src.model import Passage
from src.utils.query_expansion import expand_query
from src.search.search_strategy.abstract_search_strategy import SearchStrategy, keyword_search, vector_search

class HybridSearch(SearchStrategy):
    def search(self, request: Request, config: dict[str, Any]) -> List[Passage]:
        #config['query'] = expand_query(config['query'])
        print(f"Expanded Query: {config['query']}")

        # is_simple = classify_query(config['query'])
        # if is_simple:
        #     passages = keyword_search(request, config)
        # else:
        #     passages = vector_search(request, config)
        
        passages = vector_search(request, config)
        if not passages or len(passages) == 0:
            print("No passages found with vector search, falling back to keyword search.")
            return keyword_search(request, config)
        print(f"Vector Search Results: {len(passages)} passages found")
        return passages

