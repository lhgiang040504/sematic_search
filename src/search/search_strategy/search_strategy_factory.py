#from src.search.search_strategy.fallback_mechanism import FallbackMechanism
from src.search.search_strategy.hybrid_search import HybridSearch
from src.model import SearchStrategyType
#from src.search.search_strategy.tiered_search import TieredSearch


def get_search_strategy_map():
    return {
        SearchStrategyType.HYBRID_SEARCH: HybridSearch(),
        #SearchStrategyType.FALLBACK_MECHANISM: FallbackMechanism(),
        #SearchStrategyType.TIERED_SEARCH: TieredSearch(),
    }
