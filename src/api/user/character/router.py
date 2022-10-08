from fastapi import APIRouter

from src.resources.parse_resources import get_base_clothes
from .schemas import BaseEquipmentResponse, Item, ItemType

router = APIRouter(prefix="/character", tags=["Character"])


@router.get("/base_clothes", response_model=BaseEquipmentResponse)
async def base_clothes():
    response = BaseEquipmentResponse(
        equipment=get_base_clothes(),
    )

    return response

@router.post("/edit_description", response_model=BaseEquipmentResponse)
async def base_clothes():
    response = BaseEquipmentResponse(
        equipment=get_base_clothes(),
    )

    return response
