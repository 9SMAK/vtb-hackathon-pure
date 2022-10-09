from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status

from src.blockchain.client import generete_nft
from src.ipfs.client import get_data
from src.database.repositories import USER
from src.database.schemas import User
from src.resources.parse_resources import BASE_CLOTHES
from .schemas import BaseEquipmentResponse, CreateCharacterResponse
from src.api.auth.authentication import get_current_user, AuthenticatedUser
from src.api.user.schemas import Item
from src.api.schemas import ItemType

router = APIRouter(prefix="/character", tags=["Character"])


@router.get("/base_clothes", response_model=BaseEquipmentResponse)
async def base_clothes():
    response = BaseEquipmentResponse(
        equipment=BASE_CLOTHES,
    )

    return response


@router.post("/create_character", response_model=CreateCharacterResponse)
async def create_character(*, user: AuthenticatedUser = Depends(get_current_user), equipment: Dict[ItemType, str]):
    user_info: User = await USER.get_by_id(user.id)

    real_equipment = {}
    for t in ItemType:
        if t not in equipment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing item types",
            )

        t: ItemType
        uri = equipment[t]
        ipfs_item = await get_data(uri)
        _ = await generete_nft(_to=user_info.public_key, _uri=uri, _count=1)

        real_equipment[t] = Item(
            type=t,
            ipfs_hash=uri,
            name=ipfs_item.name,
            svg=ipfs_item.svg
        )

    resp = await USER.change_equipment(user.id, real_equipment)
    if not resp:
        return CreateCharacterResponse(
            id=user.id,
            success=False
        )

    return CreateCharacterResponse(
        id=user.id,
        success=True
    )


