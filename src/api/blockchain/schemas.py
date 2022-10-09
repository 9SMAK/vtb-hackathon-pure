from pydantic import BaseModel
from typing import Union, List
from src.api.auth.authentication import get_current_user


class BalanceResponse(BaseModel):
    user_id: int
    balance: float


class TransferDRRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float


class TransferItemRequest(BaseModel):
    sender_id: int
    receiver_id: int
    item_id: int


class TransferDRResponse(BaseModel):
    tx_id: Union[str, None] = None
    status: str
    reason: Union[str, None] = None


class Item(BaseModel):
    type: str
    name: str
    svg: str
    id: int


class InventoryResponse(BaseModel):
    user_id: int
    inventory: List[Item]
