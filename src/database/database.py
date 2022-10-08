import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src import config as cfg

logger = logging.getLogger(__name__)


class DatabaseInterface:
    def __init__(self, db_url: str) -> None:
        self._engine = create_async_engine(db_url, echo=True)
        self._sessionmaker = sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=True
        )

    def get_engine(self):
        return self._engine

    def get_sessionmaker(self):
        return self._sessionmaker


DATABASE_URL = f"postgresql+asyncpg://{cfg.POSTGRES_USER}:{cfg.POSTGRES_PASSWORD}@{cfg.POSTGRES_URL}/{cfg.POSTGRES_DB}"
DATABASE = DatabaseInterface(DATABASE_URL)
