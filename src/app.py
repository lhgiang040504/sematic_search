from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api

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

# Routers
app.include_router(api)

# Index page
@app.get("/")
def root() -> dict[str, Any]:
    return {
        "introduction": "Welcome to Semantic Search",
    }
