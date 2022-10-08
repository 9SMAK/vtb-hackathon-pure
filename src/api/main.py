import os

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, HttpUrl

from src.api import user
from src.api.schemas import HomePageResponse, SqlReturn
from src.database.client import PSQL_CLIENT
import src.config as cfg

app = FastAPI()

api_router = APIRouter(prefix="/api", tags=["API"])
api_router.include_router(user.router)
app.include_router(api_router)


@app.get("/homepage/{username}")
async def homepage(username: str):
    print(os.getenv("POSTGRES_URL"), os.getenv("POSTGRES_DB"))
    return HomePageResponse(username=username, message=f"Hello, {username}, {os.getenv('POSTGRES_DB')}")


@app.get("/{username}/coins", response_model=SqlReturn)
async def coins_value(username: str) -> SqlReturn:
    return PSQL_CLIENT.dummy_return(username)
