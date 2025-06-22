import numpy as np
from typing import List, Tuple
from src.model import PassageResponse 

def evaluate_search_quality(
    passages: List[PassageResponse],
    search_type: str,
    min_vector_score: float = 0.3,
    min_text_score: float = 1,
    min_docs_needed: int = 3,
    min_avg_score: float = 0.4,
) -> Tuple[bool, List[str]]:

    fallback_needed = False
    fallback_reason = []

    n_docs = len(passages)

    if n_docs == 0:
        fallback_needed = True
        fallback_reason.append("No documents found")
        return fallback_needed, fallback_reason

    top_score = passages[0].score
    top_n = min(3, n_docs)
    avg_score = sum([p.score for p in passages[:top_n]]) / top_n

    if search_type == "vector":
        if top_score < min_vector_score:
            fallback_needed = True
            fallback_reason.append(f"Vector top score too low: {top_score}")
        if avg_score < min_avg_score:
            fallback_needed = True
            fallback_reason.append(f"Vector avg score of top {top_n} too low: {avg_score}")
    elif search_type == "keyword":
        if top_score < min_text_score:
            fallback_needed = True
            fallback_reason.append(f"Keyword top score too low: {top_score}")

    # Small amount of documents → need soft evaluation
    if n_docs < min_docs_needed:
        if top_score >= (min_vector_score if search_type == "vector" else min_text_score):
            fallback_reason.append(f"Few documents ({n_docs}) but top score ok ({top_score}), not forcing fallback.")
        else:
            fallback_needed = True
            fallback_reason.append(f"Too few documents ({n_docs}) and top score too low.")

    return fallback_needed, fallback_reason