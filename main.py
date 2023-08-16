import json
import logging
import os
from contextlib import suppress
from pathlib import Path

import config
from remarkable.items import Collection
from remarkable.items import Document
from remarkable.client import Client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


os.makedirs(config.root_dir, exist_ok=True)


def walk_collection(collection: Collection, path: Path, client: Client):
    """Walk down a collection of collections building up a path."""
    logger.debug("Walking collection %s", collection.id or "root")
    logger.debug("Current path: %s", path)
    os.makedirs(path, exist_ok=True)

    # Recursively iterate over the collection's items and download them.
    for item in collection.items():
        if isinstance(item, Collection):
            walk_collection(item, path / item.name, client)
        elif isinstance(item, Document):
            item.package(client, path / f"{item.name}.zip")
            item.pdf(path / f"{item.name}.pdf")


with Client(config.host, config.port, config.username, config.password) as client:
    client.download_dir(Client.base_path, Path("output"))
    # walk_collection(Collection.from_root(), Path(config.root_dir), client)
