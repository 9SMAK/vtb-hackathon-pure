from fastapi import APIRouter

from src.api.schemas import OkResponse
from src.database.repositories import USER

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/create_users")
async def create_users():
    await USER.create_repository()
    return OkResponse()


@router.get("/drop_users")
async def drop_users():
    await USER.delete_repository()
    return OkResponse()


@router.get("/get_all_users")
async def get_all_users():
    result = await USER.get_all()
    return result


@router.get("/get_user_by_id")
async def get_user_by_id(user_id: int):
    result = await USER.get_by_id(user_id=user_id)
    return result


# TODO add restrictions
@router.post("/add_user")
async def add_user(nickname: str):
    await USER.add(nickname=nickname)
    return OkResponse()
