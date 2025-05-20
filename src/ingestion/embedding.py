from threading import Lock
from typing import List

import torch
from sentence_transformers import SentenceTransformer

from dotenv import dotenv_values
#config = dotenv_values("../../.env")
config = dotenv_values(".env")
model_name = config["EMBEDDING_MODEL"]
model = None
model_lock = Lock()

def generate_embedding(content: str) -> List[float]:
    global model
    model = load_embedding_model()
    return model.encode(content).tolist()


def load_embedding_model():
    global model
    if model is None:
        with model_lock:
            device = (
                torch.device("mps")
                if torch.backends.mps.is_available()
                else torch.device("cuda")
                if torch.cuda.is_available()
                else torch.device("cpu")
            )
            model = SentenceTransformer(model_name)
            model = model.to(device)
    return model

if __name__ == "__main__":
    print("---------------- generate_embedding ----------------")
    content = "Each chunk of text is converted into a vector representation using advanced embedding techniques secondly."
    embedding = generate_embedding(content)
    print(f"Content: {content}")
    print(f"Content embedding: length: {len(embedding)}")


"""
all-MiniLM-L6-v2	384
all-mpnet-base-v2	768
paraphrase-MiniLM-L3-v2	384
paraphrase-distilroberta-base-v1	768
"""