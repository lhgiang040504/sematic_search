from abc import ABC, abstractmethod
from src.chat.chatbot_abstract import prompting, get_llm_model
from langchain_core.output_parsers import StrOutputParser

from typing import Dict, Any

class BaseChain(ABC):
    def __init__(self):
        self.prompt = prompting()
        self.llm = get_llm_model()
        self.parser = StrOutputParser()

    @abstractmethod
    def set_chain(self):
        """
        Set the chain for the specific implementation.
        This method should be implemented by subclasses to define the specific chain logic.
        """
        pass

    @abstractmethod
    def retrieve(self, question: str) -> Dict[str, Any]:
        """
        Retrieve the answer to the question using the chain.
        
        Args:
            question (str): The question to be answered.
        
        Returns:
            str: The answer to the question.
        """
        pass

    def invoke(self, inputs: dict) -> str:
        """
        Invoke the chain with the given inputs.
        
        Args:
            inputs (dict): The inputs to be processed by the chain.
        
        Returns:
            str: The output of the chain.
        """
        return self.chain.invoke(inputs)