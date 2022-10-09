from fastapi import APIRouter, Depends

from src.database.repositories import USER, FRIENDS
from src.database.schemas import User
from .schemas import UsersListResponce, UsersActionResponce, CutUser
from src.api.schemas import ResponseStatus
from src.api.auth.authentication import authenticate_user, create_access_token, get_current_user, get_password_hash, \
    AuthenticatedUser

router = APIRouter(prefix="/friends", tags=["Friends"])


@router.get("/list")
async def list(current_user: AuthenticatedUser = Depends(get_current_user)):
    friends_list = await USER.get_user_friends(current_user.id)
    friends = [CutUser(id=friend.id, login=friend.login) for friend in friends_list]
    return UsersListResponce(user_id=current_user.id, users=friends)


@router.get("/incomming_requests")
async def incomming_requests(current_user: AuthenticatedUser = Depends(get_current_user)):
    user_id = current_user.id
    requests_list = await USER.get_incomming_requests(user_id)
    requests = [CutUser(id=request.id, login=request.login) for request in requests_list]
    return UsersListResponce(user_id=user_id, users=requests)


@router.get("/outcomming_requests")
async def outcomming_requests(current_user: AuthenticatedUser = Depends(get_current_user)):
    user_id = current_user.id
    requests_list = await USER.get_outcomming_requests(user_id)
    requests = [CutUser(id=request.id, login=request.login) for request in requests_list]
    return UsersListResponce(user_id=user_id, users=requests)


@router.post("/send_request")
async def send_request(*, current_user: AuthenticatedUser = Depends(get_current_user), user_to_id: int):
    user_from_id = current_user.id
    result = await FRIENDS.add(user_from_id=user_from_id, user_to_id=user_to_id, is_friends=False)
    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok if result else ResponseStatus.error
    )


@router.post("/accept_request")
async def accept_request(user_to_id: int, current_user: AuthenticatedUser = Depends(get_current_user)):
    user_from_id = current_user.id
    await FRIENDS.remove_request(user_from_id, user_to_id)
    await FRIENDS.remove_request(user_to_id, user_from_id)
    await FRIENDS.add(user_from_id=user_from_id, user_to_id=user_to_id, is_friends=True)
    await FRIENDS.add(user_from_id=user_to_id, user_to_id=user_from_id, is_friends=True)

    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )


@router.post("/cancel_request")
async def cancel_request(user_to_id: int, current_user: AuthenticatedUser = Depends(get_current_user)):
    user_from_id = current_user.id
    await FRIENDS.remove_request(user_from_id, user_to_id)

    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )


@router.post("/remove")
async def remove(user_to_id: int, current_user: AuthenticatedUser = Depends(get_current_user)):
    user_from_id = current_user.id
    await FRIENDS.remove_request(user_from_id, user_to_id)
    await FRIENDS.remove_request(user_to_id, user_from_id)
    await FRIENDS.add(user_from_id=user_to_id, user_to_id=user_from_id)

    return UsersActionResponce(
        user_from_id=user_from_id, 
        user_to_id=user_to_id, 
        status=ResponseStatus.ok
    )
