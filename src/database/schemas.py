from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    description: str = ""
    level: int = 1
    experience: int = 0
    is_admin: bool = False
    is_editor: bool = False
    is_lead: bool = False
    case_count: int = 0

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
