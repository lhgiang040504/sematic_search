from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Any

app = FastAPI(
    title="Semantic Search",
    description="Semantic Search API v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Index page
@app.get("/")
def root() -> dict[str, Any]:
    return {
        "introduction": "Welcome to Semantic Search",
    }
