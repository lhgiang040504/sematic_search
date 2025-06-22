import numpy as np
from typing import List, Set
import os

def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Compute Precision@k for a single query.
    Args:
        retrieved: List of retrieved doc_ids (ordered by rank).
        relevant: Set of relevant doc_ids (ground truth).
        k: Cutoff rank.
    Returns:
        Precision@k (float)
    """
    if k == 0:
        return 0.0
    retrieved_k = retrieved[:k]
    relevant_retrieved = [doc_id for doc_id in retrieved_k if doc_id in relevant]
    return len(relevant_retrieved) / k 

def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
    """
    Compute Recall@k for a single query.
    Args:
        retrieved: List of retrieved doc_ids (ordered by rank).
        relevant: Set of relevant doc_ids (ground truth).
        k: Cutoff rank.
    Returns:
        Recall@k (float)
    """
    if not relevant:
        return 0.0
    retrieved_k = retrieved[:k]
    relevant_retrieved = [doc_id for doc_id in retrieved_k if doc_id in relevant]
    return len(relevant_retrieved) / len(relevant)

def average_precision(retrieved: List[str], relevant: Set[str]) -> float:
    """
    Compute Average Precision (AP) for a single query.
    Args:
        retrieved: List of retrieved doc_ids (ordered by rank).
        relevant: Set of relevant doc_ids (ground truth).
    Returns:
        Average Precision (float)
    """
    if not relevant:
        return 0.0
    ap = 0.0
    num_hits = 0
    for i, doc_id in enumerate(retrieved):
        if doc_id in relevant:
            num_hits += 1
            ap += num_hits / (i + 1)
    return (ap / len(relevant))

def mean_average_precision(list_of_retrieved: List[List[str]], list_of_relevant: List[Set[str]]) -> float:
    """
    Compute Mean Average Precision (MAP) over multiple queries.
    Args:
        list_of_retrieved: List of retrieved doc_id lists (one per query).
        list_of_relevant: List of sets of relevant doc_ids (one per query).
    Returns:
        MAP (float)
    """
    if not list_of_retrieved or not list_of_relevant:
        return 0.0
    ap_scores = [average_precision(r, rel) for r, rel in zip(list_of_retrieved, list_of_relevant)]
    return float(np.mean(ap_scores)) 

def load_cranfield_ground_truth(query_id: int, res_dir: str) -> set:
    """
    Load the set of relevant doc_ids for a given query_id from the Cranfield RES directory.
    Args:
        query_id: The query number (int).
        res_dir: Path to the RES directory containing ground truth files.
    Returns:
        Set of relevant doc_ids (as strings).
    """
    relevant_docs = set()
    res_file = os.path.join(res_dir, f"{query_id}.txt")
    if not os.path.exists(res_file):
        return relevant_docs
    with open(res_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            _, doc_id, relevance = parts
            try:
                if int(relevance) > 0:
                    relevant_docs.add(doc_id)
            except ValueError:
                continue
    return relevant_docs 