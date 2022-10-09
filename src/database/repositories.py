from contextlib import AbstractContextManager
import logging
from typing import Callable, Iterator

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql.ddl import DropTable, CreateTable

from .database import DATABASE
from .tables import Friends, User
from sqlalchemy.ext.asyncio import AsyncEngine

from src.database import database


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Repository:
    _table = None

    def __init__(self, engine: AsyncEngine, sessionmaker):
        self._engine = engine
        self._sessionmaker = sessionmaker

    async def create_repository(self):
        async with self._engine.begin() as conn:
            await conn.execute(CreateTable(self._table.__table__, if_not_exists=True))

    async def delete_repository(self):
        async with self._engine.begin() as conn:
            await conn.execute(DropTable(self._table.__table__, if_exists=True))

    async def get_all(self):
        async with self._sessionmaker() as session:
            session: AsyncSession
            # async with session.begin(): - this for massive selects?
            statement = select(self._table)
            result = await session.execute(statement)
            return list(result)

    async def get_by_id(self, user_id: int) -> _table:
        async with self._sessionmaker() as session:
            statement = select(self._table).filter(self._table.id == user_id)
            res = (await session.execute(statement)).first()
            return res[0]

    # TODO add check if already exists
    async def add(self, **kwargs) -> User:
        async with self._sessionmaker() as session:
            try:
                session: AsyncSession
                new_elem= self._table(**kwargs)
                session.add(new_elem)
                await session.commit()
                await session.refresh(new_elem)
            except IntegrityError:
                await session.rollback()


class UserRepository(Repository):
    _table = User

    async def get_user_friends(self, user_id) -> Iterator[User]:
        async with self._sessionmaker() as session:
            statement = select(User).select_from(Friends).filter(Friends.user_from_id == user_id). \
                join(User, User.id == Friends.user_to_id).filter(Friends.is_friends == True)
            #friends = session.query(User).select_from(Friends).filter(Friends.user_from_id == user_id). \
            #    join(User, User.id == Friends.user_to_id).filter(Friends.is_friends == True).all()
            result = await session.execute(statement)
            return list(result)


USER = UserRepository(DATABASE.get_engine(), DATABASE.get_sessionmaker())


class FriendsRepository(Repository):
    _table = Friends


FRIENDS = FriendsRepository(DATABASE.get_engine(), DATABASE.get_sessionmaker())
