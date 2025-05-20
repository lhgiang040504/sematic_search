from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api
from src.utils.db_connection.mongodb_connector import MongoDB


# Load environment variables
from dotenv import dotenv_values
config = dotenv_values(".env")

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


# MongoDB connection
@app.on_event("startup")
def startup_db_client():
    app.mongodb = MongoDB(uri=config['MONGODB_URI'], db_name=config['MONGODB_DB'])
    app.mongodb.init()  # Initialize the MongoDB connection
    print("Connected to MongoDB database!")

    # Test
    # db = app.mongodb.get_database()
    # collection = db["documents"]  # or your collection name
    #collection.insert_one({'passage_id': 'abc', 'content': 'abc', 'doc_id': 'abc', 'embedding': [1.0, 2.0, 3.0]})
    #print("Inserted test document into MongoDB collection!")


# Close the MongoDB connection on shutdown
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb.close()  # Close the MongoDB connection
    print("Disconnected from MongoDB database!")


# Routers
app.include_router(api)


# Index page
@app.get("/")
def root() -> dict[str, Any]:
    return {
        "introduction": "Welcome to Semantic Search",
    }
