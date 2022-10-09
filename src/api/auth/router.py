from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src import config as cfg
from .schemas import RegistrationData, LoginResponse
from .authentication import authenticate_user, create_access_token, get_current_user, get_password_hash, \
    AuthenticatedUser
from src.database.repositories import USER
from src.blockchain.client import create_account

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    authenticated_user = AuthenticatedUser(id=user.id, login=user.login)

    access_token_expires = timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=authenticated_user.dict(), expires_delta=access_token_expires
    )
    return LoginResponse(
        user_id=user.id,
        access_token=access_token,
    )


@router.post("/registration")
async def registration(data: RegistrationData):
    wallet = await create_account()

    user = await USER.add(
        login=data.login,
        hashed_password=get_password_hash(data.password),
        name=data.name,
        public_key=wallet.publicKey,
        private_key=wallet.privateKey,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Login already in use",
        )


@router.get("/private/test", response_model=str)
async def private_method_example(current_user: AuthenticatedUser = Depends(get_current_user)):
    return f"You are an authenticated user! id: {current_user.id}; login: {current_user.login}"
