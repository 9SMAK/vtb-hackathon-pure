from typing import Dict

from fastapi import APIRouter, Depends

from src.database.repositories import USER
from src.resources.parse_resources import BASE_CLOTHES
from .schemas import BaseEquipmentResponse, CreateCharacterResponse
from src.api.auth.authentication import get_current_user, AuthenticatedUser
from ..schemas import Item
from ...schemas import ItemType

router = APIRouter(prefix="/character", tags=["Character"])


@router.get("/base_clothes", response_model=BaseEquipmentResponse)
async def base_clothes():
    response = BaseEquipmentResponse(
        equipment=BASE_CLOTHES,
    )

    return response


@router.post("/create_character", response_model=CreateCharacterResponse)
async def create_character(*, user: AuthenticatedUser = Depends(get_current_user), equipment: Dict[ItemType, Item]):
    resp = await USER.change_equipment(user.id, equipment)
    if not resp:
        return CreateCharacterResponse(
            id=user.id,
            success=False
        )

    return CreateCharacterResponse(
        id=user.id,
        success=True
    )


