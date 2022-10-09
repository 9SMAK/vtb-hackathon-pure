from fastapi import APIRouter, Depends

from src.resources.parse_resources import get_base_clothes
from .schemas import BaseEquipmentResponse, CreateCharacterResponse
from src.api.auth.authentication import get_current_user, AuthenticatedUser

router = APIRouter(prefix="/character", tags=["Character"])


@router.get("/base_clothes", response_model=BaseEquipmentResponse)
async def base_clothes():
    response = BaseEquipmentResponse(
        equipment=await get_base_clothes(),
    )

    return response


@router.get("/create_character", response_model=CreateCharacterResponse)
async def create_character(user: AuthenticatedUser = Depends(get_current_user)):
    return CreateCharacterResponse(
        id=user.id,
        success=True
    )


@router.post("/edit_description", response_model=BaseEquipmentResponse)
async def edit_description():
    response = BaseEquipmentResponse(
        equipment=get_base_clothes(),
    )

    return response
