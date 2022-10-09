import logging

from fastapi import APIRouter, Depends

from src.api.auth.authentication import AuthenticatedUser, get_current_user
from src.database.repositories import USER
from src.database.schemas import User
from src.blockchain.client import get_coin_balance, transfer_coins, get_nft_balance, transfer_nft
from src.ipfs.client import get_data
from src import config as cfg
from src.api.schemas import ResponseStatus
from .schemas import BalanceResponse, TransferDRRequest, TransferDRResponse, TransferItemRequest, InventoryResponse
from src.api.auth.authentication import authenticate_user, create_access_token, get_current_user, get_password_hash, \
    AuthenticatedUser
from .schemas import Item

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


async def get_public_key(user_id: int):
    user_info: User = await USER.get_by_id(user_id)
    return user_info.public_key


async def get_private_key(current_user: AuthenticatedUser = Depends(get_current_user)):
    user_info: User = await USER.get_by_id(current_user.id)
    return user_info.private_key


@router.get("/balance", response_model=BalanceResponse)
async def balance(user: AuthenticatedUser = Depends(get_current_user)):
    user_info: User = await USER.get_by_id(user.id)
    return BalanceResponse(
        user_id=user.id,
        balance=await get_coin_balance(user_info.public_key, "coins"),
    )


@router.post("/transfer/dr", response_model=TransferDRResponse)
async def transfer_dr(*, current_user: AuthenticatedUser = Depends(get_current_user), receiver_id: int, amount: float):
    if amount <= 0:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="Transfer amount should be positive number"
        )

    balance = await get_coin_balance(await get_public_key(current_user.id), "coins")
    if balance < amount:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="Not enough money on your wallet for transaction"
        )
    
    return TransferDRResponse(
        status=ResponseStatus.ok,
        tx_id=await transfer_coins(
            await get_private_key(current_user),
            await get_public_key(receiver_id),
            amount)
    )


@router.post("/transfer/item", response_model=TransferDRResponse)
async def transfer_item(*, current_user: AuthenticatedUser = Depends(get_current_user), receiver_id: int, item_id: int):
    if item_id < 0:
        return TransferDRResponse(
            status=ResponseStatus.error,
            reason="Unexisting item"
        )

    inventory = await get_nft_balance(await get_public_key(current_user.id))

    have_item = False
    for item in inventory.items:
        if item_id in item.tokens:
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
            await get_private_key(current_user),
            await get_public_key(receiver_id),
            item_id)
    )


@router.get("/inventory", response_model=InventoryResponse)
async def inventory(user_id: int):
    logging.info(f"{await get_public_key(user_id)}")
    inventory_list = await get_nft_balance(await get_public_key(user_id))

    logging.info(f"{inventory_list}")
    items = []
    for item in inventory_list.items:
        logging.info(item.uri)
        data = await get_data(item.uri)
        items.append(Item(type=data.type, name=data.name, svg=data.svg, id=item.tokens[0]))

    return InventoryResponse(user_id=user_id, inventory=items)
