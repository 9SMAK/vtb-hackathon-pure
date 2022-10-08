import json
import os
from typing import Dict, List

from src import config as cfg
from src.api.schemas import ItemType
from src.api.user.character.schemas import Item


def get_base_clothes() -> Dict[ItemType, List[Item]]:
    path = os.path.join(cfg.BASE_DIR, "resources", "data", "base_clothes.json")
    with open(path, "r", encoding="utf-8") as fp:
        data = json.load(fp)

    result = {}
    for t, items in data.items():
        result[ItemType(t)] = []
        for item in items:
            result[ItemType(t)].append(Item(
                type=item["type"],
                ipfs_hash=item["ipfs_hash"],
                name=item["name"],
                svg=item["svg"],
            ))

    return result