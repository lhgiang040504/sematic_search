from src.chat.query_router.rule_based import is_chitchat_query, is_procedural_query, is_multi_query

def classify_route_type(query: str, request, config) -> int:
    """
    Classify query into one of 4 route types:
    1 - Chitchat
    2 - Simple Query → DB Search → General LLM
    3 - MultiQuery → Fusion → LLM
    4 - Decomposition → Subqueries → LLM
    """
    if is_chitchat_query(query):
        return 1

    # is_simple = classify_simple_non_simple(query)
    # print(f"[Signal] Simple vs Non-Simple: {'Simple' if is_simple else 'Non-Simple'}")

    # Keyword-based rules
    if is_procedural_query(query):
        return 4
    if is_multi_query(query):
        return 3
    
    return 5