import imp
from fastapi import APIRouter

from src.api.user import character, friends
from src.database.repositories import USER

from .schemas import CutUser, UsersListResponce

router = APIRouter(prefix="/user")
router.include_router(character.router)
router.include_router(friends.router)


@router.get("/info", tags=["User"])
async def info():
    return None


@router.get("/workers", tags=["User"])
async def workers(user_id: int):
    workers_list = await USER.get_user_workers(user_id)
    workers = [CutUser(id=worker.id, login=worker.login) for worker in workers_list]
    return UsersListResponce(user_id=user_id, users=workers)
