import os

from fastapi import FastAPI, APIRouter, Depends
from src.api.blockchain.router import get_private_key
from src.blockchain.client import transfer_coins
from src.api.blockchain.schemas import TransferDRResponse
import src.config as cfg
 
from src.api.user import router as user_router
from src.api.auth import router as auth_router
from src.api.admin import router as admin_router
from src.api.blockchain import router as blockchain_router
from src.api.schemas import HomePageResponse, ResponseStatus, SqlReturn
from fastapi.middleware.cors import CORSMiddleware
from src.api.auth.authentication import authenticate_user, create_access_token, get_current_user, get_password_hash, \
    AuthenticatedUser

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")
api_router.include_router(user_router.router)
api_router.include_router(blockchain_router.router)
api_router.include_router(admin_router.router)
api_router.include_router(auth_router.router)
app.include_router(api_router)


@app.get("/homepage/{username}")
async def homepage(username: str):
    print(os.getenv("POSTGRES_URL"), os.getenv("POSTGRES_DB"))
    return HomePageResponse(username=username, message=f"Hello, {username}, {os.getenv('POSTGRES_DB')}")

@api_router.post("/merch/buy")
async def buy(current_user: AuthenticatedUser = Depends(get_current_user)):    
    return TransferDRResponse(
        status=ResponseStatus.ok,
        tx_id=await transfer_coins(
            get_private_key(current_user.id), 
            cfg.PUBLIC_ADMIN_KEY,
            100
        )
    )
