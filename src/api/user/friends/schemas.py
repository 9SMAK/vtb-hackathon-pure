from urllib import response
from pydantic import BaseModel, Field
from typing import List

from src.api.schemas import ItemType, ResponseStatus


class Item(BaseModel):
    type: ItemType
    ipfs_hash: str = Field(title="IPFS link for identification")
    name: str = Field(max_length=100)
    svg: str = Field(title="Image in .svg format")


class CutUser(BaseModel):
    id: int
    login: str


class UsersListResponce(BaseModel):
    user_id: int
    users: List[CutUser]


class UsersActionResponce(BaseModel):
    user_from_id: int
    user_to_id: int
    status: ResponseStatus
