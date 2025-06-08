from typing import Optional, Any
from fastapi import Request

from src.model import SearchStrategyType
from src.chat.chatbot_chain import GeneralChain, MultiQueryChain, DecompositionChain  # A factory or registry for chatbot instances
from src.search.search import search_pipeline
from src.utils.fusion_docs import get_unique_union, reciprocal_rank_fusion



def chat_pipeline(request: Request, strategy_type: SearchStrategyType, config: dict[str, Any]) -> str:
    a = 'decomposition'
    if a == 'multiquery_fusion':
        multiquery = MultiQueryChain()
        res = multiquery.retrieve(request, strategy_type, config)
        docs = res['docs']
        docs = get_unique_union(docs)
        # docs = reciprocal_rank_fusion(docs, k=60)

    elif a == 'decomposition':
        # Use single-query strategy
        decomposite = DecompositionChain()
        res = decomposite.retrieve(request, strategy_type, config)
        docs = res['docs']
        queries = res['queries']
        q_a_pairs = []
        general_chain = GeneralChain()
        for query, doc in zip(queries, docs):
            a = decomposite.invoke({"context": doc, "q_a_pairs": q_a_pairs, "question": query})
            q_a_pairs.append((query, a))
        docs = [f"{q}: {a}" for q, a in q_a_pairs]
    else:
        # Use single-query strategy
        general_chain = GeneralChain()
        docs = general_chain.retrieve(request, strategy_type, config)
        response = general_chain.invoke({"context":docs, "question":config['query']})
        return response
    
    
    # Process the message through the chatbot
    # general_chain = GeneralChain().chain
    # response = general_chain.invoke({"context":docs, "question":config['query']})
    
    return docs
