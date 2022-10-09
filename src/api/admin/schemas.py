from urllib import response
from pydantic import BaseModel, Field
from typing import List

from src.api.schemas import ItemType, ResponseStatus


class CutUser(BaseModel):
    id: int
    login: str


class UsersListResponse(BaseModel):
    user_id: int
    users: List[CutUser]


class ClaimedItem(BaseModel):
    item_name: str
    item_svg: str
    item_type: str


class ClaimCaseResponse(BaseModel):
    is_opened: bool
    claimed_item: ClaimedItem = None
