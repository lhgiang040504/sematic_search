from src.chat.base_chain import BaseChain
from src.chat.chatbot_abstract import multi_query_prompting, decomposition_question_prompting, decomposition_answer_prompting
from src.search.search import search_pipeline



class GeneralChain(BaseChain):
    def set_chain(self):
        return self.prompt | self.llm | self.parser
    
    def retrieve(self, request, strategy_type, config) -> str:
        results = search_pipeline(request, strategy_type, config)
        docs = [result.content for result in results]
    
class MultiQueryChain(BaseChain):
    def __init__(self):
        super().__init__()
        self.prompt = multi_query_prompting()
        self.chain = self.set_chain()

    def set_chain(self):
        # Multi Query: Different Perspectives
        return self.prompt | self.llm | self.parser | (lambda x: x.split("\n"))
    
    def retrieve(self, request, strategy_type, config) -> str:
        queries = self.chain.invoke({"question": config['query']})
        docs = []
        
        for query in queries:
            # Process each query through the search pipeline
            results = search_pipeline(request, strategy_type, {**config, 'query': query})
            patial_docs = [result.content for result in results]
            docs.append(patial_docs)

        return {
            'queries': queries,
            'docs': docs,
            'scores': [result.score for result in results],
        }
    

class DecompositionChain(BaseChain):
    def __init__(self):
        super().__init__()
        self.prompt = decomposition_question_prompting()
        self.chain = self.set_chain()

    def set_chain(self):
        # Decomposition Question
        return self.prompt | self.llm | self.parser | (lambda x: x.split("\n"))
    
    def retrieve(self, request, strategy_type, config) -> str:
        queries = self.chain.invoke({"question": config['query']})
        docs = []
        
        for query in queries:
            # Process each query through the search pipeline
            results = search_pipeline(request, strategy_type, {**config, 'query': query})
            patial_docs = [result.content for result in results]
            docs.append(patial_docs)

        # Decomposition Answer
        self.prompt = decomposition_answer_prompting()
        self.chain = self.set_chain()

        return {
            'queries': queries,
            'docs': docs,
            'scores': [result.score for result in results],
        }
    