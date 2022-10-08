from fastapi import APIRouter, Query

from src.blockchain.client import get_coin_balance
from .schemas import BalanceResponse, TransferDRRequest, TransferDRResponse

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


def get_user_key(user_id: int):
    public_admin_key = "0xdEE1415af0534B5EDa0995b8682BDB8a3d9498E5"
    return public_admin_key


@router.get("/balance", response_model=BalanceResponse)
async def balance(user_id: int):
    return BalanceResponse(
        user_id=user_id,
        balance=await get_coin_balance(get_user_key(user_id), "coins"),
    )


@router.post("/transfer", response_model=TransferDRResponse)
async def transfer(data: TransferDRRequest):
    return TransferDRResponse(
        status="ok"
    )
