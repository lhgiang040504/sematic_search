import os
from threading import Lock

from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments


from dotenv import dotenv_values
#config = dotenv_values("../../.env")
config = dotenv_values(".env")
model_name = config["EMBEDDING_MODEL"]

model_dir = "query_classification_model"
train_dir = "query_classification_results"

dataset_path = "microsoft/ms_marco"
dataset_name = "v1.1"
tokenizer = None
tokenizer_lock = Lock()


def train_query_classification():
    if os.path.exists(model_dir):
        print("Loading existing model...")
        model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    else:
        print("Initializing new model...")
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    train_dataset, test_dataset = prepare_train_test_dataset()

    training_args = TrainingArguments(
        output_dir=train_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )

    trainer.train()

    model.save_pretrained(model_dir)


def is_trained():
    return os.path.exists(model_dir)


def prepare_train_test_dataset() -> tuple[Dataset, Dataset]:
    global tokenizer
    dataset = load_dataset(dataset_path, dataset_name)  # Replace with your dataset name
    tokenizer = load_tokenizer()

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    train_data = prepare_data(dataset, "train", max_samples=5000)
    train_dataset = Dataset.from_dict(train_data)
    train_dataset = train_dataset.map(tokenize_function, batched=True)
    train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    test_data = prepare_data(dataset, "test", max_samples=1000)
    test_dataset = Dataset.from_dict(test_data)
    test_dataset = test_dataset.map(tokenize_function, batched=True)
    test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    return train_dataset, test_dataset


def load_tokenizer():
    global tokenizer
    if tokenizer is None:
        with tokenizer_lock:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer


def prepare_data(input_dataset, split="train", max_samples=5000):
    queries = input_dataset[split]["query"][:max_samples]
    labels = [1 if qt == "description" else 0 for qt in input_dataset[split]["query_type"][:max_samples]]
    return {"text": queries, "label": labels}


if __name__ == "__main__":
    train_query_classification()