from fastapi import APIRouter

from src.api.user import character

router = APIRouter(prefix="/user", tags=["User"])
router.include_router(character.router)


@router.get("/info")
async def info():
    return None
