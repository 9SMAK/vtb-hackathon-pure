import imp
from fastapi import APIRouter, Depends
from src.api.auth.authentication import get_current_user
from src.api.auth.authentication import AuthenticatedUser

from src.api.auth.authentication import AuthenticatedUser, get_current_user
from src.api.admin.schemas import ClaimCaseResponse, ClaimedItem
from src.api.user.character import router as character_router
from src.api.user.friends import router as friends_router
from src.database.repositories import USER
from src.ipfs.client import get_data
from src.resources.parse_resources import get_random_item


from ...blockchain.client import generete_nft
from .schemas import CutUser, UsersListResponce, UserInfoResponse

router = APIRouter(prefix="/user")
router.include_router(character_router.router)
router.include_router(friends_router.router)


# TODO safe auth
@router.post("/claim_case", response_model=ClaimCaseResponse)
async def claim_case(user_id: int):
    is_opened = True
    # is_opened = await USER.decrease_case_cnt_safe(user_id)
    # if not is_opened:
    #     return ClaimCaseResponse(is_opened=is_opened)

    item_hash = get_random_item()
    item = await get_data(item_hash)

    user_public_key = (await USER.get_by_id(user_id)).public_key
    await generete_nft(_to=user_public_key, _uri=item_hash, _count=1)

    claimed_item = ClaimedItem(item_name=item.name, item_svg=item.svg, item_type=item.type)
    return ClaimCaseResponse(is_opened=is_opened,
                             claimed_item=claimed_item)

                         
@router.get("/info", tags=["User"])
async def info(user_id: int):
    user_info = await USER.get_by_id(user_id)

    return UserInfoResponse(**user_info.dict())


# @router.post("/edit_description", response_model=)
# async def edit_description(description: str):
#     response = BaseEquipmentResponse(
#         equipment=get_base_clothes(),
#     )
#
#     return response


@router.get("/workers", tags=["User"])
async def workers(current_user: AuthenticatedUser = Depends(get_current_user)):
    user_id = current_user.id
    workers_list = await USER.get_user_workers(user_id)
    workers = [CutUser(id=worker.id, login=worker.login) for worker in workers_list]
    return UsersListResponce(user_id=user_id, users=workers)
