from pathlib import Path

import requests

from remarkable.client import Client
from remarkable.items.item import Item


class Document(Item):
    """
    A document on the remarkable.
    """
    def pdf(self, path: Path):
        """Obtain document as PDF."""
        document = requests.get(f"http://10.11.99.1/download/{self.id}/placeholder")
        with open(path, "wb") as f:
            f.write(document.content)

    def package(self, client: Client, path: Path):
        client.notebook(self.id, path)
