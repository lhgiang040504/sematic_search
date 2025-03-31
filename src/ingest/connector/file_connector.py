from typing import List, Iterator
from unstructured.partition.auto import partition # A function from the unstructured library that extracts text from files.

from src.ingest.connector.abstract_connector import Connector
from src.model import Document

class FileConnector(Connector):
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths

    def load_data(self) -> Iterator[Document]:
        for file_path in self.file_paths:
            try:
                elements = partition(file_path)
                content = "\n".join([element.text for element in elements if element.text])

                # Create a Passage object for each file
                yield Document(
                    doc_id=file_path,
                    content=content
                )
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")