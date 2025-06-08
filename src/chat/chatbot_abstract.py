from langchain import hub
from langchain.prompts import ChatPromptTemplate
from langchain_together import ChatTogether


def prompting() -> str:
    """
    A function to handle the prompting logic.
    
    Args:
        prompt (str): The prompt to be processed.
        **kwargs: Additional keyword arguments for future use.
        
    Returns:
        str: The processed prompt.
    """
    # For now, just return the prompt as is
    # Prompt
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    return ChatPromptTemplate.from_template(template)

def multi_query_prompting() -> str:
    """
    A function to handle the multi-query prompting logic.
    
    Args:
        prompt (str): The prompt to be processed.
        **kwargs: Additional keyword arguments for future use.
        
    Returns:
        str: The processed prompt.
    """
    # Multi Query: Different Perspectives
    template = """You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines. Original question: {question}"""
    
    return ChatPromptTemplate.from_template(template)

def decomposition_question_prompting() -> str:
    """
    A function to handle the decomposition question prompting logic.
    
    Args:
        prompt (str): The prompt to be processed.
        **kwargs: Additional keyword arguments for future use.
        
    Returns:
        str: The processed prompt.
    """
    # Decomposition Question
    template = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
    The goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \n
    Generate multiple search queries related to: {question} \n
    Output (3 queries):"""
    
    return ChatPromptTemplate.from_template(template)

def decomposition_answer_prompting() -> str:
    """
    A function to handle the decomposition answer prompting logic.
    
    Args:
        prompt (str): The prompt to be processed.
        **kwargs: Additional keyword arguments for future use.
        
    Returns:
        str: The processed prompt.
    """
    # Decomposition Answer
    template = """Here is the question you need to answer:

    \n --- \n {question} \n --- \n

    Here is any available background question + answer pairs:

    \n --- \n {q_a_pairs} \n --- \n

    Here is additional context relevant to the question: 

    \n --- \n {context} \n --- \n

    Use the above context and any background question + answer pairs to answer the question: \n {question}
    """
    
    return ChatPromptTemplate.from_template(template)


# Get llm model
def get_llm_model(model_name: str = "mistralai/Mixtral-8x7B-Instruct-v0.1"):
    """
    A function to retrieve a language model from LangChain hub.
    
    Args:
        model_name (str): The name of the model to retrieve.
        
    Returns:
        The language model instance.
    """
    #return hub.pull(model_name)
    return ChatTogether(model=model_name)
