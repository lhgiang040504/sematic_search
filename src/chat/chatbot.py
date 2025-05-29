from typing import Optional
from fastapi import Request
from src.model import SearchStrategyType


from src.chat.chatbot_chain import Chain  # A factory or registry for chatbot instances
from src.search.search import search_pipeline


def chat_pipeline(request: Request, strategy_type: SearchStrategyType, max_results: int, message: str, session_id: Optional[str] = None) -> str:
    # Get the chatbot instance (can be a singleton, session-based, etc.)
    chain = Chain().set_chain()

    # Process the message through the chatbot
    results = search_pipeline(request, strategy_type, message, max_results)
    docs = [result.content for result in results]
    response = chain.invoke({"context":docs, "question":message})

    return response
