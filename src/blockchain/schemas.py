from enum import auto
from pydantic import BaseModel


class AccountInfo(BaseModel):
    privateKey: str
    publicKey: str


class Item(BaseModel):
    uri: str
    tokens: list


class Inventory(BaseModel):
    items: list[Item]


class HistoryItem(BaseModel):
    timeStamp: int
    from_user: str
    to_user: str
    value: int
    tokenName: str
    tokenSymbol: str


class History(BaseModel):
    items: list[HistoryItem]


class NftInfo(BaseModel):
    tokenId: int
    uri: str
    publicKey: str