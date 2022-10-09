from urllib import response
from pydantic import BaseModel, Field
from typing import List

from src.api.schemas import ItemType, ResponseStatus


class User(BaseModel):
    id: int
    nickname: str


class UsersListResponce(BaseModel):
    user_id: int
    users: List[User]
