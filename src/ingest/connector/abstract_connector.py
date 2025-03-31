from abc import ABC, abstractmethod
from typing import Iterator
from src.model import Document

class Connector(ABC):
    """Abstract base class for data connectors."""

    @abstractmethod
    def load_data(self) -> Iterator[Document]:
        """Loads data and yields Document instances."""
        pass