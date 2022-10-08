from urllib import response
from fastapi import APIRouter

from .schemas import User, UsersListResponce, UsersActionResponce
from src.api.schemas import ResponseStatus

router = APIRouter(prefix="/friends", tags=["Friends"])


@router.get("/list", response_model=UsersListResponce)
async def list(user_id: int):
    friends_list = []   # database.api.users.get_user_friends(user_id)
    return UsersListResponce(user_id=user_id, users=friends_list)


@router.get("/incomming_requests", response_model=UsersListResponce)
async def incomming_requests(user_id: int):
    request_list = []   # database.api.users.get_user_incomming_requests(user_id)
    return UsersListResponce(user_id=user_id, users=request_list)


@router.get("/outcomming_requests", response_model=UsersListResponce)
async def outcomming_requests(user_id: int):
    request_list = []   # database.api.users.get_user_outcomming_requests(user_id)
    return UsersListResponce(user_id=user_id, users=request_list)


@router.post("/send_request", response_model=UsersActionResponce)
async def send_request(user_from_id: int, user_to_id: int):
    # database.api.friends.add_request(user_from_id, user_to_id, is_friends=False)
    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )


@router.post("/accept_request", response_model=UsersActionResponce)
async def accept_request(user_from_id: int, user_to_id: int):
    # database.api.friends.accept_request(user_from_id, user_to_id, is_friends=False)
    #
    # OR
    #
    # delete_request(user_from_id, user_to_id) + add_request(user_from_id, user_to_id, True) + add_request(user_to_id, user_from_id, True)

    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )


@router.post("/cansel_request", response_model=UsersActionResponce)
async def cansel_request(user_from_id: int, user_to_id: int):
    # database.api.friends.delete_request(user_from_id, user_to_id)

    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )


@router.post("/remove", response_model=UsersActionResponce)
async def remove(user_from_id: int, user_to_id: int):
    # database.api.friends.delete_request(user_from_id, user_to_id) + -/-.delete_request(user_to_id, user_from_id) 
    #
    # Should we create request from user_to to user_from? (Like in vk): -/-.add_request(user_to_id, user_from_id, False)

    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )


#@router.post("/add", response_model=UsersActionResponce)
#async def add(user_from_id: int, user_to_id: int):
#    # database.api.friends.delete_request(user_from_id, user_to_id)
#
#    return UsersActionResponce(
#        user_from_id=user_from_id, 
#        user_to_id=user_to_id, 
#        status=ResponseStatus.ok
#    )
#