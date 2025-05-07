from typing import Optional, Iterator
from datasets import load_dataset
# from huggingface_hub import login
# from dotenv import dotenv_values
# config = dotenv_values(".env")

# #login(config['HUGGINGFACE_TOKEN'])

from src.ingestion.connector.abstract_connector import Connector
from src.utils.hash import generate_md5_hash
from src.model import Document


class HuggingFaceConnector(Connector):
    def __init__(self, dataset_path: str, dataset_name: str, split: str, max_size: Optional[int] = 1000, chunk_size: Optional[int] = 1000):
        self.dataset_path = dataset_path
        self.dataset_name = dataset_name
        self.split = split
        self.max_size = max_size
        self.chunk_size = chunk_size

    def load_data(self) -> Iterator[Document]:
        dataset = load_dataset(self.dataset_path, name=self.dataset_name, split=self.split)
        # Limits how many records to process
        print(len(dataset))
        max_idx = min(len(dataset), self.max_size)
        for start_idx in range(0, max_idx, self.chunk_size):
            rows = dataset.select(range(start_idx, min(start_idx + self.chunk_size, max_idx)))
            for row in rows:
                for index, doc_content in enumerate(row["passages"]["passage_text"]):
                    # TODO: dynamic mapping function for each dataset
                    yield to_passage(doc_content)


# Refer: https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train
# answers,passages,query,query_id,query_type,wellFormedAnswers
# [Results-Based...],{"is_selected":[0,1,0...],"passage_text":["Since 2007,the RBA..."],"url":["https://en.wikipedia.org..."]},what is rba,19699,description,[]
def to_passage(doc_content: str) -> Document:
    return Document(
        doc_id=generate_md5_hash(doc_content),
        content=doc_content
    )