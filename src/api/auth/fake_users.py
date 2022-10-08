from typing import Dict, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    password: str
    name: str


fake_users_db: Dict[str, User] = {}
global_id = 1


async def add_user(login, hashed_password, name) -> Optional[User]:
    global global_id
    if login in fake_users_db:
        return None

    fake_users_db[login] = User(
        id=global_id,
        login=login,
        password=hashed_password,
        name=name,
    )
    global_id += 1
    return fake_users_db[login]


async def get_user_by_login(login):
    return fake_users_db.get(login)
