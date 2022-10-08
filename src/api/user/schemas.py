from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class UserRights(BaseModel):
    is_admin: bool
    is_editor: bool
    is_headmaster: bool


class Event(BaseModel):
    label: str = Field(max_length=100)
    description: str = Field(max_length=1000)


class Achievement(BaseModel):
    label: str = Field(max_length=100)
    description: str = Field(max_length=1000)
    image: str = Field(title="Image in .svg format")


class UserInfoResponse(BaseModel):
    id: int
    login: str
    description: str = Field(title="The description of the item", max_length=500)
    level: int
    experience: int
    rights: UserRights
    equipment: List[str] = Field(title="List of equipped items")
    case_count: int
    events: List[Event]
    friends: List[str]
    achievements: List[Achievement]
