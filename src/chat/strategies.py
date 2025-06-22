import logging
from src.chat.prompts import PROMPTS, get_llm_model
from src.search.search import search_pipeline
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class BaseStrategy:
    def __init__(self, prompt_key: str):
        self.prompt = PROMPTS[prompt_key]
        self.llm = get_llm_model()
        self.parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.parser

    def invoke(self, inputs: dict):
        logger.info(f"Invoking LLM chain with inputs: {list(inputs.keys())}")
        return self.chain.invoke(inputs)

class GeneralStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("general")

    def retrieve(self, strategy_type, config):
        logger.info(f"GeneralStrategy retrieving with strategy_type: {strategy_type}")
        results = search_pipeline(strategy_type, config)
        docs = [result.content for result in results]
        return docs

class ChitChatStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("chitchat")

    def response(self, query: str):
        logger.info(f"ChitChatStrategy responding to query: {query}")
        return self.invoke({"question": query})

class MultiQueryStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("multi_query")

    def retrieve(self, strategy_type, config):
        logger.info(f"MultiQueryStrategy retrieving for query: {config.get('query')}")
        queries = self.invoke({"question": config["query"]}).split("\n")
        docs = []
        for query in queries:
            results = search_pipeline(strategy_type, {**config, "query": query})
            docs.append([result.content for result in results])
        return queries, docs

class DecompositionStrategy(BaseStrategy):
    def __init__(self):
        super().__init__("decomposition_question")

    def retrieve(self, strategy_type, config):
        logger.info(f"DecompositionStrategy retrieving for query: {config.get('query')}")
        queries = self.invoke({"question": config["query"]}).split("\n")
        docs = []
        for query in queries:
            results = search_pipeline(strategy_type, {**config, "query": query})
            docs.append([result.content for result in results])
        return queries, docs

    def answer(self, context, q_a_pairs, question):
        logger.info(f"DecompositionStrategy answering for question: {question}")
        self.prompt = PROMPTS["decomposition_answer"]
        self.chain = self.prompt | self.llm | self.parser
        return self.invoke({"context": context, "q_a_pairs": q_a_pairs, "question": question}) 