from threading import Lock

import torch
from transformers import AutoModelForSequenceClassification

from src.search.query_classification.complex_classification.train import model_dir, load_tokenizer

model = None
model_lock = Lock()


# 1: simple -> run with inverted index search
# 0: complex -> run with semantic index search
def classify_query(query: str) -> int:
    global model
    tokenizer = load_tokenizer()
    inputs = tokenizer(query, return_tensors='pt', truncation=True, padding=True, max_length=128)

    with torch.no_grad():
        model = load_query_classification_model()
        outputs = model(**inputs)

    logits = outputs.logits
    return torch.argmax(logits, dim=1).item()


def load_query_classification_model():
    global model
    if model is None:
        with model_lock:
            model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    return model