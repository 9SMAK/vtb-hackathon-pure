from fastapi import APIRouter

from src.api.schemas import OkResponse
from src.database.repositories import USER, FRIENDS
from .schemas import UsersListResponce, User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/create_users")
async def create_users():
    await USER.create_repository()
    return OkResponse()


@router.get("/drop_users")
async def drop_users():
    await USER.delete_repository()
    return OkResponse()


@router.get("/get_user_by_id")
async def get_user_by_id(user_id: int):
    result = await USER.get_by_id(user_id=user_id)
    return result


# TODO add restrictions
@router.post("/add_user")
async def add_user(nickname: str):
    await USER.add(nickname=nickname)
    return OkResponse()

@router.get("/get_all_users")
async def get_all_users():
    result = await USER.get_all()
    return result


@router.get("/get_user_by_id")
async def get_user_by_id(user_id: int):
    result = await USER.get_by_id(user_id=user_id)
    return result

@router.get("/get_user_friends")
async def get_user_by_id(user_id: int):
    friends_list = await USER.get_user_friends(user_id=user_id)
    friends = [User(id=friend.User.id, nickname=friend.User.nickname) for friend in friends_list]
    return UsersListResponce(user_id=user_id, users=friends)


@router.get("/create_friends")
async def create_friends():
    await FRIENDS.create_repository()
    return OkResponse()


@router.get("/drop_friends")
async def drop_friends():
    await FRIENDS.delete_repository()
    return OkResponse()


@router.get("/get_all_friends")
async def get_all_friends():
    result = await FRIENDS.get_all()
    return result

# TODO add restrictions
@router.post("/add_friends")
async def add_friends(user_from_id: int, user_to_id: int, is_friends: bool):
    await FRIENDS.add(user_from_id=user_from_id, user_to_id=user_to_id, is_friends=is_friends)
    return OkResponse()
