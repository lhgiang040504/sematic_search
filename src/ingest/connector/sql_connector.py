from typing import AsyncIterator
import asyncpg

from src.ingest.connector.abstract_connector import Connector
from src.model import Document

class SQLConnector(Connector):
    def __init__(self, connection_string: str, query: str):
        self.connection_string = connection_string
        self.query = query

    async def load_data(self) -> AsyncIterator[Document]:
        conn = await asyncpg.connect(self.connection_string)
        async with conn.transaction():
            async for record in conn.cursor(self.query):
                yield Document(
                    doc_id=record['doc_id'],
                    content=record['content']
                )
        await conn.close()