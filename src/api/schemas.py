from enum import auto
from pydantic import BaseModel
from fastapi_utils.enums import CamelStrEnum


class OkResponse(BaseModel):
    result: str = 'ok'


class HomePageResponse(BaseModel):
    username: str
    message: str


class SqlReturn(BaseModel):
    username: str
    value: int


class ItemType(CamelStrEnum):
    hair = auto()
    head = auto()
    body = auto()
    bottom = auto()
    shoes = auto()

class ResponseStatus(CamelStrEnum):
    ok = auto()
    error = auto()
