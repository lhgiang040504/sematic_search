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
