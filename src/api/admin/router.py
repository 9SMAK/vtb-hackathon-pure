from fastapi import APIRouter

from src.api.schemas import OkResponse
from src.database.repositories import USER, FRIENDS, RELATIONSHIPS
from .schemas import UsersListResponce, CutUser
from src.database.schemas import User

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
async def get_user_by_id(user_id: int) -> User:
    result = await USER.get_by_id(user_id=user_id)
    return result


# TODO add restrictions
@router.post("/add_user")
async def add_user(login: str, password: str, name: str):
    res = await USER.add(login=login, hashed_password=password, name=name)
    return res


@router.get("/create_friends")
async def create_friends():
    await FRIENDS.create_repository()
    return OkResponse()


@router.get("/drop_friends")
async def drop_friends():
    await FRIENDS.delete_repository()
    return OkResponse()


@router.get("/get_all_relationships")
async def get_all_relationships():
    result = await RELATIONSHIPS.get_all()
    return result


@router.get("/create_relationships")
async def create_relationships():
    await RELATIONSHIPS.create_repository()
    return OkResponse()


@router.get("/drop_relationships")
async def drop_relationships():
    await RELATIONSHIPS.delete_repository()
    return OkResponse()


@router.get("/add_relationship")
async def add_relationship(lead_id: int, worker_id: int):
    result = await RELATIONSHIPS.add(lead=lead_id, worker=worker_id)
    return OkResponse()
