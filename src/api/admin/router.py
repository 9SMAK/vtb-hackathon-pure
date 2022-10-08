from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Event"])


@router.get("/info")
async def info():
    return None
