from pydantic import BaseModel, Field
from typing import Dict, List

from src.api.schemas import ItemType


class Item(BaseModel):
    ipfs_uri: str = Field(title="IPFS link for identification")
    label: str = Field(max_length=100)
    image: str = Field(title="Image in .svg format")


class BaseEquipmentResponse(BaseModel):
    equipment: Dict[ItemType, List[Item]]
