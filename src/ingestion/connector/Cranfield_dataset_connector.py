import os
from typing import Iterator
from src.model import Document
from src.utils.hash import generate_md5_hash
from src.ingestion.connector.abstract_connector import Connector


class Cranfield(Connector):
    def __init__(self, dataset_folderpath: str):
        self.name = "Cranfield"

        file_paths = []
        if os.path.isdir(dataset_folderpath):
            for root, _, files in os.walk(dataset_folderpath):
                for file in files:
                    file_paths.append(os.path.join(root, file))
        else:
            print(f"error: '{dataset_folderpath}' not exit.")

        self.dataset_filepaths = file_paths

    def load_data(self) -> Iterator[Document]:
        for file_path in self.dataset_filepaths:
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                filename = os.path.basename(file_path)
                doc_id = os.path.splitext(filename)[0]  # '1.txt' → '1'
                doc_id = f"cranfield{int(doc_id):04d}"  # '1' → 'cranfield0001'

                yield Document(
                    doc_id=doc_id,
                    content=content
                )
