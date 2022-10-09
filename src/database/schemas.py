from typing import List, Dict

from pydantic import BaseModel

from src.api.schemas import ItemType
from src.api.user.schemas import Item


class User(BaseModel):
    id: int
    login: str
    hashed_password: str
    name: str
    description: str = ""
    level: int = 1
    experience: int = 0
    is_admin: bool = False
    is_editor: bool = False
    is_lead: bool = False
    case_count: int = 0
    public_key: str
    private_key: str
    equipment: Dict[ItemType, Item] = {}

    class Config:
        orm_mode = True


class Friends(BaseModel):
    id: int
    user_from_id: int
    user_to_id: int
    is_friends: bool

    class Config:
        orm_mode = True


class Achievement(BaseModel):
    id: int
    name: str
    description: str = ""
    svg: str

    class Config:
        orm_mode = True


class Merch(BaseModel):
    id: int
    description: str
    image: str
    price: float

    class Config:
        orm_mode = True


class Event(BaseModel):
    id: int
    title: str
    description: str = ""
    type: str
    members: List[int] = []

    class Config:
        orm_mode = True


class Relationships(BaseModel):
    id: int
    lead: int
    worker: int

    class Config:
        orm_mode = True
