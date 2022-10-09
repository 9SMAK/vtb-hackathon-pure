from fastapi import APIRouter

from src.api.user import character, friends

router = APIRouter(prefix="/user")
router.include_router(character.router)
router.include_router(friends.router)


@router.get("/info", tags=["User"])
async def info():
    return None
