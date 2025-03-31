from typing import List, AsyncIterator

import aiohttp
from bs4 import BeautifulSoup

from src.ingest.connector.abstract_connector import Connector
from src.model import Document

class HTMLConnector(Connector):
    def __init__(self, urls: List[str], div_selector: str):
        self.urls = urls
        self.div_selector = div_selector

    async def load_data(self) -> AsyncIterator[Document]:
        async with aiohttp.ClientSession() as session:
            for url in self.urls:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    div_content = soup.select_one(self.div_selector).get_text(strip=True)
                    yield Document(
                        doc_id=url,
                        content=div_content
                    )