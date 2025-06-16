# 🧠 Retrieval-Augmented Generation (RAG) System

This project implements a modular **Retrieval-Augmented Generation (RAG)** system using traditional and neural search techniques, integrated with prompt-based query handling. It is designed for question-answering and document retrieval tasks.

---

## 📘 Overview

Our RAG system combines:

- **Keyword & Vector Search**: to retrieve relevant documents.
- **Prompt Pipelines**: to process the queries with various strategies.
- **Flexible Routing**: to intelligently select the best processing method.

---

## 📂 Datasets

The system supports multiple document corpora:

- **MS MARCO**: A large-scale passage ranking dataset.
- **Cranfield**: A classic IR dataset for evaluating retrieval models.

---

## 🔍 Search Pipeline

- **Vector Search**: Using sentence embeddings and similarity metrics.
- **Keyword Search**: Based on tokenized, indexed text fields and BM25.

---

## 🧾 Prompt Pipeline

- **General**: Single-turn question answering.
- **Multi Query**: Splits user query into multiple sub-queries.
- **Decomposition**: Decomposes complex questions into logical steps.

---

## ⚙️ Installation & Running

### 1. Clone the Repository

```bash
git clone
cd
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

---

## 🚀 Running the System

### A. Start Backend Server

Ensure your virtual environment is active:

```bash
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

Then launch the backend:

```bash
python main.py
```

This will start the FastAPI server at:
[http://localhost:8000](http://localhost:8000)

### B. Start Frontend Client (if applicable)

If your project includes a frontend (e.g., Vite/React):

```bash
cd client
npm install
npm run dev
```

Access the frontend at:
[http://localhost:3000](http://localhost:3000)
