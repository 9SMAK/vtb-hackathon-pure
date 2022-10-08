import json

import src.config as cfg
import aiohttp

from .schemas import *
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(3))
async def send_request(method: str, url: str, **kwargs) -> any:
    async with aiohttp.ClientSession() as session:
        return await session.request(
                method=method,
                url=url,
                verify_ssl=False,
                timeout=5,
                **kwargs
        )


async def get_data(_id: str):
    """
        :return dict
        {
            "type": "shoes",
            "name": "2",
            "svg": "<>"
        }
    """
    resp = await send_request('POST', cfg.IPFS_URL + f'/api/v0/get?arg={_id}&progress=true')
    string = await resp.text()
    item_info = json.loads(f'{{ {string.split("{")[1].split("}")[0]} }}')
    return Item(
        type=item_info["type"],
        name=item_info["name"],
        svg=item_info["svg"]
    )

#
# async def main():
#     re = await get_data('QmY8ucSJwPxqVzjSS9MxKnLRSkGXE5SJTZFkb8KjrEvtvc')
#     print(re)
#
# if __name__ == '__main__':
#     asyncio.run(main())