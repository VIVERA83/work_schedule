import logging

from typing import Any, Optional, Union, Literal

from sqlalchemy.engine import Result
from sqlalchemy.orm import MappedColumn
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.sql.elements import TextClause

from sqlalchemy import (
    insert,
    select,
    update,
    delete,
    text,
    func,
)

from .types import Model, Query
from core.settings import PostgresSettings


class PostgresAccessor:
    _engine: Optional[AsyncEngine] = None
    settings: Optional[PostgresSettings] = None

    def __init__(self, logger: logging.Logger):
        self.settings = PostgresSettings()
        self.logger = logger

    async def connect(self):
        self._engine = create_async_engine(
            self.settings.dsn(True),
            echo=True,
            future=True,
        )
        self.logger.info(
            f"{self.__class__.__name__} {self.settings.dsn()} подключился к базе данных"
        )

    async def disconnect(self):
        if self._engine:
            await self._engine.dispose()

        self.logger.info(f"{self.__class__.__name__} отключился от базы данных")

    @property
    def session(self) -> AsyncSession:
        return async_sessionmaker(bind=self._engine, expire_on_commit=False)()

    @staticmethod
    def get_query_insert(model: Model, **insert_data) -> Query:
        return insert(model).values(**insert_data)

    @staticmethod
    def get_query_select_by_model(model: Model) -> Query:
        return select(model)

    @staticmethod
    def get_query_select_by_fields(
        select_field: Union[MappedColumn, Literal["*"]], *select_fields: MappedColumn
    ) -> Query:
        return select(select_field, *select_fields)

    @staticmethod
    def get_query_update(model: Model, **update_data) -> Query:
        return update(model).values(**update_data)

    @staticmethod
    def get_query_delete(model: Model) -> Query:
        return delete(model)

    async def query_execute(self, query: Union[Query, TextClause]) -> Result[Any]:
        async with self.session as session:
            result = await session.execute(query)
            await session.commit()
            return result

    async def query_executes(self, *query: Query) -> list[Result[Any]]:
        async with self.session as session:
            result = [await session.execute(q) for q in query]
            await session.commit()
            return result

    @staticmethod
    def get_query_from_text(smtp: str) -> TextClause:
        return text(smtp)

    @staticmethod
    def get_query_random(model: Model, count: int = 1) -> Query:
        return select(model).order_by(func.random()).limit(count)
