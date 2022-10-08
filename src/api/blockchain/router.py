from fastapi import APIRouter

from src.blockchain.client import get_coin_balance, transfer_coins, get_nft_balance, transfer_nft
from src.ipfs.client import get_data
from src import config as cfg
from src.api.schemas import ResponseStatus
from .schemas import BalanceResponse, TransferDRRequest, TransferDRResponse, TransferItemRequest, InventoryResponse

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


def get_public_key(user_id: int):
    public_admin_key = "0xdEE1415af0534B5EDa0995b8682BDB8a3d9498E5"
    return public_admin_key


def get_private_key(user_id: int):
    private_admin_key = cfg.PRIVATE_KEY
    return private_admin_key


@router.get("/balance", response_model=BalanceResponse)
async def balance(user_id: int):
    return BalanceResponse(
        user_id=user_id,
        balance=await get_coin_balance(get_public_key(user_id), "coins"),
    )


@router.post("/transfer/dr", response_model=TransferDRResponse)
async def transfer_dr(data: TransferDRRequest):
    if data.amount <= 0:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="Transfer amount should be positive number"
        )

    balance = await get_coin_balance(get_public_key(data.sender_id), "coins")
    if balance < data.amount:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="Not enough money on your wallet for transaction"
        )
    
    return TransferDRResponse(
        status=ResponseStatus.ok,
        tx_id=await transfer_coins(
            get_private_key(data.sender_id), 
            get_public_key(data.receiver_id),
            data.amount)
    )


@router.post("/transfer/item", response_model=TransferDRResponse)
async def transfer_item(data: TransferItemRequest):
    if data.item_id < 0:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="Unexisting item"
        )

    inventory = await get_nft_balance(get_public_key(data.sender_id))

    have_item = False
    for item in inventory.items:
        if data.item_id in item.tokens:
            have_item = True
            break
    
    if not have_item:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="You don't have specific item in your inventory"
        )
    
    return TransferDRResponse(
        status=ResponseStatus.ok,
        tx_id=await transfer_nft(
            get_private_key(data.sender_id), 
            get_public_key(data.receiver_id),
            data.item_id)
    )


@router.get("/inventory", response_model=InventoryResponse)
async def inventory(user_id: int):
    inventory = await get_nft_balance(get_public_key(user_id))

    items = []
    for item in inventory.items:
        items += [await get_data(id) for id in item.tokens]

    return InventoryResponse(user_id=user_id, inventory=items)
