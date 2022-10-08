from fastapi import APIRouter

router = APIRouter(prefix="/event", tags=["Event"])


@router.get("/info")
async def info():
    return None
