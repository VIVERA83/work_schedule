from logging import Logger

from uuid import UUID

from store.db.postgres.accessor import PostgresAccessor
from store.db.postgres.types import Model
from store.ws.base.exceptions import exception_handler, NotFoundException


class BaseAccessor:
    class Meta:
        model: Model = None

    def __init__(self, accessor: PostgresAccessor, loger: Logger):
        self.__accessor = accessor
        self.logger = loger
        self.logger.info(f"{self.__class__.__name__} инициализирован.")

    @property
    def accessor(self) -> "PostgresAccessor":
        return self.__accessor

    @exception_handler()
    async def create(self, **fields: dict) -> Model:
        model = self.Meta.model(**fields)
        async with self.accessor.session as session:
            session.add(model)
            await session.commit()
        self.logger.info(f"Создан {self.Meta.model.__name__} с полями {fields}")
        return model

    @exception_handler(NotFoundException)
    async def update(self, id_: int, **fields: dict) -> Model:
        smtp = (
            self.accessor.get_query_update(self.Meta.model)
            .where(self.Meta.model.id == id_)  # noqa
            .values(**fields)
            .returning(self.Meta.model)
        )
        result = await self.accessor.query_execute(smtp)
        self.logger.info(f"Обновлен {self.Meta.model.__name__} с id {id_}")
        return result.scalars().one()

    @exception_handler()
    async def delete_by_id(self, id_: int | str | UUID) -> Model:
        smtp = (
            self.accessor.get_query_delete(self.Meta.model)
            .where(self.Meta.model.id == id_)  # noqa
            .returning(self.Meta.model)
        )
        result = await self.accessor.query_execute(smtp)
        self.logger.info(f"Удален {self.Meta.model.__name__} с id {id_}")
        return result.scalars().one()

    @exception_handler()
    async def get_by_id(self, id_: int | str | UUID) -> Model:
        smtp = self.accessor.get_query_select_by_fields("*").filter(
            self.Meta.model.id == id_
        )  # noqa
        result = await self.accessor.query_execute(smtp)
        return self.Meta.model(**result.mappings().one())
