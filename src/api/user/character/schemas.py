from pydantic import BaseModel, Field
from typing import Dict, List

from src.api.schemas import ItemType


class Item(BaseModel):
    type: ItemType
    ipfs_hash: str = Field(title="IPFS link for identification")
    name: str = Field(max_length=100)
    svg: str = Field(title="Image in .svg format")


class BaseEquipmentResponse(BaseModel):
    equipment: Dict[ItemType, List[Item]]


class CreateCharacterResponse(BaseModel):
    id: int
    success: bool
