from pydantic import BaseModel
from typing import Union, List
from src.ipfs.schemas import Item as IPFS_Item


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


class InventoryResponse(BaseModel):
    user_id: int
    inventory: List[IPFS_Item]