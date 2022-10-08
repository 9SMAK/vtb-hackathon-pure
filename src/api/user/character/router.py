from fastapi import APIRouter

from .schemas import BaseEquipmentResponse, Item, ItemType

router = APIRouter(prefix="/character", tags=["Character"])


@router.get("/base_clothes", response_model=BaseEquipmentResponse)
async def base_clothes():
    response = BaseEquipmentResponse(
        equipment={
            ItemType.hat: [Item(ipfs_uri="ipfs://test1", label="Hat 1", image=""),
                           Item(ipfs_uri="ipfs://test2", label="Hat 2", image="")],
            ItemType.head: [Item(ipfs_uri="ipfs://test3", label="Head 1", image="")],
            ItemType.body: [Item(ipfs_uri="ipfs://test4", label="Body 1", image="")],
            ItemType.bottom: [Item(ipfs_uri="ipfs://test5", label="Bottom 1", image="")],
            ItemType.shoes: [Item(ipfs_uri="ipfs://test6", label="Shoes 1", image="")],
        }
    )

    return response
