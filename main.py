import logging
import os
from pathlib import Path

import config
from remarkable.client import Client
from remarkable.items import Collection
from remarkable.items import Document

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

root_dir = Path(config.root_dir)
os.makedirs(root_dir, exist_ok=True)
os.makedirs(root_dir / "dump", exist_ok=True)
os.makedirs(root_dir / "trove" / "pdf", exist_ok=True)
os.makedirs(root_dir / "trove" / "rmn", exist_ok=True)


def walk_collection(
    collection: Collection,
    path: Path,
    client: Client,
    rmn: bool,
    pdf: bool,
):
    """Walk down a collection of collections building up a path."""
    logger.debug("Walking collection %s", collection.id or "root")
    logger.debug("Current path: %s", path)
    os.makedirs(path, exist_ok=True)

    # Recursively iterate over the collection's items and download them.
    for item in collection.items(client):
        if isinstance(item, Collection):
            walk_collection(item, path / item.name, client, rmn=rmn, pdf=pdf)
        elif isinstance(item, Document):
            if rmn:
                item.rmn(client, path / f"{item.name}.rmn")
            if pdf:
                item.pdf(path / f"{item.name}.pdf")


with Client(config.host, config.port, config.username, config.password) as client:
    if config.dump:
        client.download_dir(
            Path("."),
            root_dir / "dump",
        )
    if config.trove:
        walk_collection(
            Collection.from_root(),
            root_dir / "trove" / "rmn",
            client,
            rmn=True,
            pdf=False
        )
        walk_collection(
            Collection.from_root(),
            root_dir / "trove" / "pdf",
            client,
            rmn=False,
            pdf=True
        )
