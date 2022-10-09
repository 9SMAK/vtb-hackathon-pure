import aiofiles
import json
import os
from typing import Dict, List

from src import config as cfg
from src.api.schemas import ItemType
from src.api.user.character.schemas import Item


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
