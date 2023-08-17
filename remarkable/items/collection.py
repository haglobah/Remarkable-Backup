from typing import Iterator

import requests

import config
from remarkable.client import Client
from remarkable.items.document import Document
from remarkable.items.item import Item


class Collection(Item):
    """
    A folder on the remarkable.
    """

    @classmethod
    def from_root(cls):
        """Collection from the root directory."""
        return cls.dummy()

    @property
    def items_url(self):
        """Fetch the URL where the items in the collection live."""
        if self.is_dummy:
            return f"http://{config.host}/documents/"
        else:
            return f"http://{config.host}/documents/{self.id}"

    def items(self, client: Client) -> Iterator[Item]:
        """Iterate through the collection's items."""
        for item in requests.post(self.items_url).json():
            match item["Type"]:
                case "DocumentType":
                    yield Document(item)
                case "CollectionType":
                    yield Collection(item)
