from fastapi import APIRouter, Query

from schemas import BalanceResponse, TransferDRRequest, TransferDRResponse

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


@router.get("/balance", response_model=BalanceResponse)
async def balance(user_id: int):
    return BalanceResponse(
        user_id=user_id,
        balance=0,
    )


@router.post("/transfer", response_model=TransferDRResponse)
async def transfer(data: TransferDRRequest):
    return TransferDRResponse(
        status="ok"
    )
