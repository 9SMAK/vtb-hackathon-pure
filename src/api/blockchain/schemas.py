from pydantic import BaseModel


class BalanceResponse(BaseModel):
    user_id: int
    balance: float


class TransferDRRequest(BaseModel):
    sender_id: int
    receiver_id: int


class TransferDRResponse(BaseModel):
    status: str
