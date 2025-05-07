from pymongo import MongoClient
from pymongo.database import Database

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client: MongoClient | None = None
        self.database: Database | None = None

    def init(self):
        """Initialize MongoDB connection"""
        if not self.client:
            self.client = MongoClient(self.uri)
        if not self.database:
            self.database = self.client[self.db_name]

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

    def get_database(self) -> Database:
        assert self.database is not None, "Database not initialized"
        return self.database