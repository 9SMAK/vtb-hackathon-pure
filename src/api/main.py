import os

from fastapi import FastAPI, APIRouter

from src.api import user, blockchain, admin, auth
from src.api.schemas import HomePageResponse, SqlReturn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api", tags=["API"])
api_router.include_router(user.router)
api_router.include_router(blockchain.router)
api_router.include_router(admin.router)
api_router.include_router(auth.router)
app.include_router(api_router)


@app.get("/homepage/{username}")
async def homepage(username: str):
    print(os.getenv("POSTGRES_URL"), os.getenv("POSTGRES_DB"))
    return HomePageResponse(username=username, message=f"Hello, {username}, {os.getenv('POSTGRES_DB')}")
