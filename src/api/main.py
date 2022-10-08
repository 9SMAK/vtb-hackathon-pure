from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


@app.get("/homepage/{username}")
async def update_item(username: str):
    return {
        "username": username,
        "message": f"Hello, {username}"
    }
