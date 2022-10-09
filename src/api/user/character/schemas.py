from pydantic import BaseModel
from typing import Dict, List

from src.api.schemas import ItemType
from src.api.user.schemas import Item


class BaseEquipmentResponse(BaseModel):
    equipment: Dict[ItemType, List[Item]]


class CreateCharacterResponse(BaseModel):
    id: int
    success: bool
