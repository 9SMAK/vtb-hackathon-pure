from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field

from src.api.schemas import ItemType


class Event(BaseModel):
    label: str = Field(max_length=100)
    description: str = Field(max_length=1000)


class Achievement(BaseModel):
    label: str = Field(max_length=100)
    description: str = Field(max_length=1000)
    image: str = Field(title="Image in .svg format")


class Item(BaseModel):
    type: ItemType
    ipfs_hash: str = Field(title="IPFS link for identification")
    name: str = Field(max_length=100)
    svg: str = Field(title="Image in .svg format")


class UserInfoResponse(BaseModel):
    id: int
    login: str
    name: str
    description: str = Field(title="The description of the item", max_length=500)
    level: int
    experience: int
    is_admin: bool
    is_editor: bool
    is_lead: bool
    equipment: Dict[ItemType, Item] = Field(title="Dict of equipped items")
    case_count: int
    # events: List[Event]
    # friends: List[str]
    # achievements: List[Achievement]


class CutUser(BaseModel):
    id: int
    login: str


class UsersListResponce(BaseModel):
    user_id: int
    users: List[CutUser]
