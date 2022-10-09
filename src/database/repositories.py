import logging
from typing import List, Dict

from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.sql.ddl import DropTable, CreateTable

import src.database.schemas as schemas
from .database import DATABASE
from .tables import Friends, User, Relationships
from sqlalchemy.ext.asyncio import AsyncEngine

from src.database import database
from src.api.schemas import ItemType
from src.api.user.schemas import Item

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Repository:
    _table = None
    _pydantic_schema = BaseModel

    def __init__(self, engine: AsyncEngine, sessionmaker):
        self._engine = engine
        self._sessionmaker = sessionmaker

    async def create_repository(self):
        async with self._engine.begin() as conn:
            await conn.execute(CreateTable(self._table.__table__, if_not_exists=True))

    async def delete_repository(self):
        async with self._engine.begin() as conn:
            await conn.execute(DropTable(self._table.__table__, if_exists=True))

    async def get_all(self) -> List[_pydantic_schema]:
        async with self._sessionmaker() as session:
            session: AsyncSession
            # async with session.begin(): - this for massive selects?
            statement = select(self._table)
            result = await session.execute(statement)
            return self._pydantic_convert_list(result)

    async def get_by_id(self, id: int) -> _pydantic_schema:
        async with self._sessionmaker() as session:
            statement = select(self._table).filter(self._table.id == id)
            res = (await session.execute(statement)).first()
            return self._pydantic_convert_object(res)

    # TODO add check if already exists
    async def add(self, **kwargs) -> bool:
        async with self._sessionmaker() as session:
            try:
                session: AsyncSession
                new_elem = self._table(**kwargs)
                session.add(new_elem)
                await session.commit()
                await session.refresh(new_elem)
                return True
            except IntegrityError:
                await session.rollback()
                return False

    def _pydantic_convert_object(self, sqlalchemy_object):
        return self._pydantic_schema.from_orm(sqlalchemy_object[0])

    def _pydantic_convert_list(self, sqlalchemy_list):
        return [self._pydantic_schema.from_orm(x[self._table.__name__]) for x in sqlalchemy_list]


class UserRepository(Repository):
    _table = User
    _pydantic_schema = schemas.User

    async def get_by_login(self, login: str) -> _pydantic_schema:
        async with self._sessionmaker() as session:
            statement = select(self._table).filter(self._table.login == login)
            res = (await session.execute(statement)).first()
            return self._pydantic_convert_object(res)

    async def get_user_friends(self, user_id) -> List[_pydantic_schema]:
        async with self._sessionmaker() as session:
            statement = select(User).select_from(Friends).filter(Friends.user_from_id == user_id). \
                join(User, User.id == Friends.user_to_id).filter(Friends.is_friends == True)
            result = await session.execute(statement)
            return self._pydantic_convert_list(result)

    # TODO typings
    async def decrease_case_cnt_safe(self, user_id: int):
        async with self._sessionmaker() as session:
            try:
                statement = update(self._table).where(
                    self._table.id == user_id
                ).values(case_count=self._table.case_count - 1)
                await session.execute(statement)
                await session.commit()
                await session.flush()
                return True
            except IntegrityError:
                await session.rollback()
                return False

    async def change_description(self, user_id: int, description: str):
        async with self._sessionmaker() as session:
            try:
                statement = update(self._table).where(
                    self._table.id == user_id
                ).values(description=description)
                await session.execute(statement)
                await session.commit()
                await session.flush()
                return True
            except IntegrityError:
                await session.rollback()
                return False

    async def change_equipment(self, user_id: int, equipment: Dict[ItemType, Item]):
        async with self._sessionmaker() as session:
            try:
                statement = update(self._table).where(
                    self._table.id == user_id
                ).values(equipment=equipment)
                await session.execute(statement)
                await session.commit()
                await session.flush()
                return True
            except IntegrityError:
                await session.rollback()
                return False

    async def get_incomming_requests(self, user_id) -> List[_pydantic_schema]:
        async with self._sessionmaker() as session:
            statement = select(User).select_from(Friends).filter(Friends.user_to_id == user_id). \
                join(User, User.id == Friends.user_from_id).filter(Friends.is_friends == False)
            result = await session.execute(statement)
            return self._pydantic_convert_list(result)

    async def get_outcomming_requests(self, user_id) -> List[_pydantic_schema]:
        async with self._sessionmaker() as session:
            statement = select(User).select_from(Friends).filter(Friends.user_from_id == user_id). \
                join(User, User.id == Friends.user_to_id).filter(Friends.is_friends == False)
            result = await session.execute(statement)
            return self._pydantic_convert_list(result)

    async def get_user_workers(self, user_id) -> List[_pydantic_schema]:
        async with self._sessionmaker() as session:
            statement = select(User).select_from(Relationships).filter(Relationships.lead == user_id). \
                join(User, User.id == Relationships.worker)
            result = await session.execute(statement)
            return self._pydantic_convert_list(result)


USER = UserRepository(DATABASE.get_engine(), DATABASE.get_sessionmaker())


class FriendsRepository(Repository):
    _table = Friends
    _pydantic_schema = schemas.Friends

    async def remove_request(self, user_from_id, user_to_id):
        async with self._sessionmaker() as session:
            statement = delete(Friends).where(Friends.user_from_id == user_from_id, Friends.user_to_id == user_to_id)
            await session.execute(statement)
            await session.commit()
            await session.flush()


FRIENDS = FriendsRepository(DATABASE.get_engine(), DATABASE.get_sessionmaker())


class RelationshipsRepository(Repository):
    _table = Relationships
    _pydantic_schema = schemas.Relationships


RELATIONSHIPS = RelationshipsRepository(DATABASE.get_engine(), DATABASE.get_sessionmaker())
