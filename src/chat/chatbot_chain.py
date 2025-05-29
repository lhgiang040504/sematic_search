from typing import Optional
from src.chat.chatbot_abstract import prompting, get_llm_model

from langchain_core.output_parsers import StrOutputParser


class Chain:
    def __init__(self):
        """
        Initialize the Chain class.
        This can be extended to include any necessary setup or configuration.
        """
        self.prompt = prompting()
        self.llm = get_llm_model()

    def set_chain(self):
        chain = self.prompt | self.llm | StrOutputParser()
        return chain
