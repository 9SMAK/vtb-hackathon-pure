import imp
from fastapi import APIRouter

from src.api.admin.schemas import ClaimCaseResponse, ClaimedItem
from src.api.user import character, friends
from src.database.repositories import USER
from src.ipfs.client import get_data
from src.resources.parse_resources import get_random_item


from .schemas import CutUser, UsersListResponce
from ...blockchain.client import generete_nft

router = APIRouter(prefix="/user")
router.include_router(character.router)
router.include_router(friends.router)


# TODO safe auth
@router.post("/claim_case", response_model=ClaimCaseResponse)
async def claim_case(user_id: int):
    is_opened = await USER.decrease_case_cnt_safe(user_id)
    if not is_opened:
        return ClaimCaseResponse(is_opened=is_opened)

    item_hash = get_random_item()
    item = await get_data(item_hash)

    user_public_key = await USER.get_by_id(user_id).public_key
    await generete_nft(_to=user_public_key, _uri=item_hash, _count=1)

    claimed_item = ClaimedItem(item_name=item.name, item_svg=item.svg, item_type=item.type)
    return ClaimCaseResponse(is_opened=is_opened,
                             claimed_item=claimed_item)


@router.get("/info", tags=["User"])
async def info():
    return None


@router.get("/workers", tags=["User"])
async def workers(user_id: int):
    workers_list = await USER.get_user_workers(user_id)
    workers = [CutUser(id=worker.id, login=worker.login) for worker in workers_list]
    return UsersListResponce(user_id=user_id, users=workers)
