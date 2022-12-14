import asyncio

import aiohttp

from .schemas import *
from tenacity import retry, stop_after_attempt

base_url = 'https://hackathon.lsp.team/hk'


@retry(stop=stop_after_attempt(3))
async def send_request(method: str, url: str, **kwargs) -> any:
    async with aiohttp.ClientSession() as session:
        async with session.request(
                method=method,
                url=url,
                verify_ssl=False,
                timeout=5,
                **kwargs
        ) as response:
            return await response.json()


async def create_account():
    """
        :return dict {"privateKey": "3243", "publicKey": "47655"}
    """
    info = await send_request('POST', base_url + '/v1/wallets/new')
    return AccountInfo(privateKey=info["privateKey"], publicKey=info["publicKey"])


async def transfer_coins(_from: str, _to: str, _amount: float):
    """
        :param _from: user private key: str
        :param _to: user public key: str
        :param _amount: float
        :return: tx_id string
    """
    resp = await send_request('POST', base_url + '/v1/transfers/ruble',
                              json={
                                  "fromPrivateKey": _from,
                                  "toPublicKey": _to,
                                  "amount": _amount
                              })
    return resp['transaction']


async def transfer_nft(_from: str, _to: str, _id: int):
    """
        :param _from: user private key: str
        :param _to: user public key: str
        :param _id: int
        :return: tx_id string
    """
    resp = await send_request('POST', base_url + '/v1/transfers/nft',
                              json={
                                  "fromPrivateKey": _from,
                                  "toPublicKey": _to,
                                  "tokenId": _id
                              })
    return resp['transaction_hash']


async def get_coin_balance(_pub_key: str, _token: str):
    """
        :param _pub_key: Public key: str
        :param _token: Can be 'matic' or 'coins': str
        :return: float. Balance: str
    """
    if _token not in ['matic', 'coins']:
        pass

    resp = await send_request('GET', base_url + f'/v1/wallets/{_pub_key}/balance')
    return resp[f'{_token}Amount']


async def get_nft_balance(_pub_key: str):
    """
        :param _pub_key: Public key: str
        :return: Balance: list

        "balance": [
            {
                "URI": "ipfs://bafybeifesqvvmmtcjlmeso3zaqh56mhttgza2eglw7zwy4ryuyifduy4i/images/star.png",
                "tokens": [5, 3, 4, 6]
            }
        ]
    """
    resp = await send_request('GET', base_url + f'/v1/wallets/{_pub_key}/nft/balance')
    return Inventory(items=[Item(uri=item['uri'], tokens=item['tokens']) for item in resp['balance']])


async def generete_nft(_to: str, _uri: str, _count: int):
    """
        :param _to: user public key: str
        :param _uri: str
        :param _count: int
        :return: tx_id string
    """
    resp = await send_request('POST', base_url + '/v1/nft/generate',
                              json={
                                  "toPublicKey": _to,
                                  "uri": _uri,
                                  "nftCount": _count
                              })
    return resp['transaction_hash']


async def get_tx_history(_user: str):
    """
        :param _user: user public key: str
        :return: history list

        [
            {
              "blockNumber": 0,
              "timeStamp": 0,
              "contractAddress": "string",
              "from": "0x15Cc4abzz27647ec9fE70D892E55586074263dF0",
              "to": "0x15Cc4abzz27647ec9fE70D892E55586074263dF0",
              "value": 7777090721429512000,
              "tokenName": "Wrapped Matic",
              "tokenSymbol": "WMATIC",
              "gasUsed": 120026,
              "confirmations": 4920439
            }
        ]
    """
    resp = await send_request('POST', base_url + f'/v1/wallets/{_user}/history',
                              json={
                                  "page": 1,
                                  "offset": 20,
                                  "sort": "asc"
                              })
    return History(items=[
        HistoryItem(
            timeStamp=item['timeStamp'],
            from_user=item['from'],
            to_user=item['to'],
            value=item['value'],
            tokenName=item['tokenName'],
            tokenSymbol=item['tokenSymbol'],
        ) for item in resp['history']])


async def get_nft_info(_id: str):
    """
        :param _id: token id: int
        :return: info dict

        {
            "tokenId": 5,
            "uri": "ipfs://bafybeifesqvvmmtcjlmeso3zaqh56mhttgza2eglw7zwy4ryuyifduy4i/images/star.png",
            "publicKey": "0x15Cc4abzz27647ec9fE70D892E55586074263dF0"
        }
    """
    info = await send_request('GET', base_url + f'/v1/nft/{_id}')
    return NftInfo(
        tokenId=info["tokenId"],
        uri=info["uri"],
        publicKey=info["publicKey"],
    )

# async def main():
#     # re = await get_nft_balance(
#     #     _pub_key="0xdEE1415af0534B5EDa0995b8682BDB8a3d9498E5"
#     # )
#     # print(re)
#
#     re = await generete_nft(
#         _to="0x9F6eEc850d46E10a053057D69a90290D011127B4",
#         _uri="QmRqbVLHmapdyHpDHF2vJ5mRsbm6SX7Jt5PxvHSxS4UQWr",
#         _count=1
#     )
#     print(re)
#
# if __name__ == '__main__':
#     asyncio.run(main())