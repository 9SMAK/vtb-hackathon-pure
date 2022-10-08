from fastapi import APIRouter

from src.api.user import character, friends

router = APIRouter(prefix="/user", tags=["User"])
router.include_router(character.router)
router.include_router(friends.router)


@router.get("/info")
async def info():
    return None
