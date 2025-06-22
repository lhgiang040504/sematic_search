from typing import Any
from fastapi import Request
from src.model import SearchStrategyType
from src.chat.strategies import GeneralStrategy, MultiQueryStrategy, DecompositionStrategy, ChitChatStrategy
from src.chat.query_router.rule_based import is_chitchat_query, is_multi_query, is_procedural_query
from src.chat.query_router.valid_query import is_valid_natural_language_query, detect_language
from src.utils.fusion_docs import reciprocal_rank_fusion
import logging
from prefect import flow

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def validate_query(query: str) -> str | None:
    if not query or query.strip() == "":
        return "⚠️ You have not entered a valid question. Please try again."
    if not is_valid_natural_language_query(query):
        return "⚠️ The question is invalid or not in natural language. Please try again."
    return None

# def check_language(query: str) -> str | None:
#     lang = detect_language(query)
#     if lang not in ["en"]:
#         return f"⚠️ The system currently only supports English. Detected language: {lang}"
#     return None

@flow(name="Chat Pipeline")
def chat_pipeline_flow(strategy_type: SearchStrategyType, config: dict[str, Any]) -> str:
    query = config.get('query', '')
    logger.info(f"Chat pipeline started for query: {query}")
    # Step 1: Validate query
    error = validate_query(query)
    if error:
        logger.warning(f"Validation failed for query: {query} - {error}")
        return error
    # Step 2: Check language
    # lang_error = check_language(query)
    # if lang_error:
    #     logger.warning(f"Language check failed for query: {query} - {lang_error}")
    #     return lang_error
    # Step 3: Handle chitchat
    if is_chitchat_query(query):
        logger.info(f"Chitchat detected for query: {query}")
        chitchat = ChitChatStrategy()
        return chitchat.response(query)
    # Step 4: Retrieve docs
    if is_procedural_query(query):
        logger.info(f"Multi-query detected for query: {query}")
        multiquery = MultiQueryStrategy()
        queries, docs = multiquery.retrieve(strategy_type, config)
        docs = reciprocal_rank_fusion(docs, k=60)
        context = docs
    else:
        logger.info(f"Decomposition strategy used for query: {query}")
        decomp = DecompositionStrategy()
        queries, docs = decomp.retrieve(strategy_type, config)
        q_a_pairs = []
        for q, doc in zip(queries, docs):
            a = decomp.answer(doc, q_a_pairs, q)
            q_a_pairs.append((q, a))
        context = [f"{q}: {a}" for q, a in q_a_pairs]
    # Step 5: Generate answer
    logger.info(f"Generating answer for query: {query}")
    general = GeneralStrategy()
    answer = general.invoke({"context": context, "question": query})
    logger.info(f"Chat pipeline completed for query: {query}")
    return answer
    

def chat_pipeline(request: Request, strategy_type: SearchStrategyType, config: dict[str, Any]) -> str:
    return chat_pipeline_flow(strategy_type, config)
