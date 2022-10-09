from fastapi import APIRouter

from src.api.admin.schemas import ClaimCaseResponse, ClaimedItem
from src.api.user import character, friends
from src.database.repositories import USER
from src.ipfs.client import get_data
from src.resources.parse_resources import get_random_item

router = APIRouter(prefix="/user", tags=["User"])
router.include_router(character.router)
router.include_router(friends.router)


# TODO safe auth
@router.post("/claim_case", response_model=ClaimCaseResponse)
async def claim_case(user_id: int):
    is_opened = await USER.decrease_case_cnt_safe(user_id)
    if not is_opened:
        return ClaimCaseResponse(is_opened=is_opened)

    item_hash = get_random_item()
    # item = await get_data(item_hash)
    # claimed_item = ClaimedItem(item_name=item.name, item_svg=item.svg, item_type=item.type)
    # TODO remove follow and uncomment above:
    claimed_item = ClaimedItem(item_name=item_hash, item_svg="<tmp_svg>", item_type="<tmp_type>")

    return ClaimCaseResponse(is_opened=is_opened,
                             claimed_item=claimed_item)
