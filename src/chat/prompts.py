from langchain.prompts import ChatPromptTemplate
from langchain_together import ChatTogether

def get_llm_model(model_name: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
    return ChatTogether(model=model_name)

PROMPTS = {
    "general": ChatPromptTemplate.from_template(
        """Answer the question based only on the following context:\n{context}\n\nQuestion: {question}"""
    ),
    "chitchat": ChatPromptTemplate.from_template(
        """You are a friendly and engaging AI assistant. Have a natural and human-like conversation with the user.\nAnswer the user input in a helpful and polite manner.\n\nUser: {question}\n\nAI:"""
    ),
    "multi_query": ChatPromptTemplate.from_template(
        """You are an AI language model assistant. Your task is to generate five \ndifferent versions of the given user question to retrieve relevant documents from a vector \ndatabase. By generating multiple perspectives on the user question, your goal is to help\nthe user overcome some of the limitations of the distance-based similarity search. \nProvide these alternative questions separated by newlines. Original question: {question}"""
    ),
    "decomposition_question": ChatPromptTemplate.from_template(
        """You are a helpful assistant that generates multiple sub-questions related to an input question. \nThe goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \nGenerate multiple search queries related to: {question} \nOutput (3 queries):"""
    ),
    "decomposition_answer": ChatPromptTemplate.from_template(
        """Here is the question you need to answer:\n\n---\n{question}\n---\n\nHere is any available background question + answer pairs:\n\n---\n{q_a_pairs}\n---\n\nHere is additional context relevant to the question: \n\n---\n{context}\n---\n\nUse the above context and any background question + answer pairs to answer the question: \n{question}"""
    ),
} 