from enum import auto
from pydantic import BaseModel


class Item(BaseModel):
    type: str
    name: str
    svg: str
