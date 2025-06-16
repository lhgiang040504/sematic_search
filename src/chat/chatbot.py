from typing import Optional, Any
from fastapi import Request

from src.model import SearchStrategyType
from src.chat.chatbot_chain import GeneralChain, MultiQueryChain, DecompositionChain, ChitChatChain  # A factory or registry for chatbot instances
from src.search.search import search_pipeline
from src.utils.fusion_docs import get_unique_union, reciprocal_rank_fusion
from src.chat.query_router.rule_based import is_chitchat_query, is_procedural_query, is_multi_query
from src.chat.query_router.valid_query import is_valid_natural_language_query, detect_language
from src.chat.query_router.translate import translate_to_english

from prefect import flow, task, get_run_logger

# === Define Prefect Tasks === #

@task
def validate_query(query: str) -> Optional[str]:
    if not query or query.strip() == "":
        return "⚠️ You have not entered a valid question. Please try again."
    if not is_valid_natural_language_query(query):
        return "⚠️ The question is invalid or not in natural language. Please try again."
    return None

@task
def detect_and_check_language(query: str) -> Optional[str]:
    lang = detect_language(query)
    if lang not in ["fi"]:
        return f"⚠️ The system currently only supports English. Detected language: {lang}"
    return None

@task
def handle_chitchat(query: str) -> str:
    chitchat = ChitChatChain()
    return chitchat.response(query)['response']

@task
def handle_multi_query(request: Request, strategy_type: SearchStrategyType, config: dict[str, Any]):
    multiquery = MultiQueryChain()
    res = multiquery.retrieve(request, strategy_type, config)
    docs = reciprocal_rank_fusion(res['docs'], k=60)
    return docs

@task
def handle_single_query(request: Request, strategy_type: SearchStrategyType, config: dict[str, Any]):
    decomposite = DecompositionChain()
    res = decomposite.retrieve(request, strategy_type, config)
    docs = res['docs']
    queries = res['queries']
    q_a_pairs = []
    for query, doc in zip(queries, docs):
        a = decomposite.invoke({"context": doc, "q_a_pairs": q_a_pairs, "question": query})
        q_a_pairs.append((query, a))
    docs = [f"{q}: {a}" for q, a in q_a_pairs]
    return docs

@task
def get_final_answer(docs: list[str], question: str) -> str:
    chain = GeneralChain().set_chain()
    return chain.invoke({"context": docs, "question": question})

# === Define the Main Flow === #

@flow(name="Chatbot Interaction Pipeline")
def chat_pipeline(request: Request, strategy_type: SearchStrategyType, config: dict[str, Any]) -> str:
    logger = get_run_logger()
    query = config.get('query', '')

    # Step 1: Validate query
    error = validate_query(query)
    if error:
        logger.warning(error)
        return error

    # Step 2: Check language
    lang_error = detect_and_check_language(query)
    if lang_error:
        logger.warning(lang_error)
        return lang_error

    # Step 3: Handle chitchat
    if is_chitchat_query(query):
        return handle_chitchat(query)

    # Step 4: Retrieve docs
    if is_multi_query(query):
        docs = handle_multi_query(request, strategy_type, config)
    else:
        docs = handle_single_query(request, strategy_type, config)

    # Step 5: Generate answer
    return get_final_answer(docs, query)


# def chat_pipeline(request: Request, strategy_type: SearchStrategyType, config: dict[str, Any]) -> str:
#     query = config['query']
#     #route_strategy = route_engine(config)

#     # Preprocessing step
#     if not query or query.strip() == "":
#         return "⚠️ You have not entered a valid question. Please try again."

#     if not is_valid_natural_language_query(query):
#         return "⚠️ The question is invalid or not in natural language. Please try again."

#     lang = detect_language(query)
#     print(lang)
#     if lang not in ["fi"]:
#         return f"⚠️ The system currently only supports English. Detected languages:"
    
#     #query = translate_to_english(query)
#     if is_chitchat_query(query):
#         chitchat = ChitChatChain()
#         res = chitchat.response(query)
#         return res['response']
#     if is_multi_query(query):
#         multiquery = MultiQueryChain()
#         res = multiquery.retrieve(request, strategy_type, config)
#         docs = res['docs']
#         #docs = get_unique_union(docs)
#         docs = reciprocal_rank_fusion(docs, k=60)

#     else:
#         # Use single-query strategy
#         decomposite = DecompositionChain()
#         res = decomposite.retrieve(request, strategy_type, config)
#         docs = res['docs']
#         queries = res['queries']
#         q_a_pairs = []
#         general_chain = GeneralChain()
#         for query, doc in zip(queries, docs):
#             a = decomposite.invoke({"context": doc, "q_a_pairs": q_a_pairs, "question": query})
#             q_a_pairs.append((query, a))
#         docs = [f"{q}: {a}" for q, a in q_a_pairs]
    
#         # # Use single-query strategy
#         # general_chain = GeneralChain()
#         # docs = general_chain.retrieve(request, strategy_type, config)
#         # response = general_chain.set_chain().invoke({"context":docs, "question":config['query']})
#         # return response
    
    
#     #Process the message through the chatbot
#     general_chain = GeneralChain().set_chain()
#     response = general_chain.invoke({"context":docs, "question":config['query']})
    
#     #print(f"Chat response: {docs}")
#     return response
