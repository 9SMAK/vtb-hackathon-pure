import aiofiles
import json
import os
from typing import Dict, List
import random

from src import config as cfg
from src.api.schemas import ItemType
from src.api.user.character.schemas import Item
from src.resources.cases import RARITY_TO_PROB


async def get_base_clothes() -> Dict[ItemType, List[Item]]:
    path = os.path.join(cfg.BASE_DIR, "resources", "data", "base_clothes.json")
    async with aiofiles.open(path, "r", encoding="utf-8") as fp:
        data = json.loads(await fp.read())

    result = {}
    for t in ItemType:
        if t not in data:
            continue

        t: ItemType
        result[t] = []
        for item in data[t]:
            result[t].append(Item(
                type=item["type"],
                ipfs_hash=item["ipfs_hash"],
                name=item["name"],
                svg=item["svg"],
            ))

    return result


def get_case_items():
    """
    Return hashes and probabilities
    """
    path = os.path.join(cfg.BASE_DIR, "resources", "data", "case_items.json")
    with open(path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
        return [el["ipfs_hash"] for el in data["items"]], [1 / RARITY_TO_PROB[el["rarity"]] for el in data["items"]]


HASHES, WEIGHTS = get_case_items()


def get_random_item() -> str:
    return random.choices(population=HASHES, weights=WEIGHTS, k=1)[0]
