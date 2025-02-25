from logging import Logger
from typing import Any

from api.base.schemes import PAGE, PAGE_SIZE
from api.base.types import EndpointType, ParamsType
from fastapi import APIRouter

from manager.base.manager import BaseManager
from store.work_schedule.base.accessor import BaseAccessor


class BaseView(APIRouter):
    class Meta:
        manager: BaseManager
        store: BaseAccessor
        endpoints: EndpointType | dict[str, ParamsType]

    def __init__(
            self,
            prefix: str,
            tags: list[str],
            logger: Logger,
    ):
        super().__init__(prefix=prefix, tags=tags)
        self.logger = logger
        self.__init_meta_class()

    def __init_meta_class(self):
        try:
            self.store = getattr(self.Meta, "store")
        except AttributeError:
            self.logger.debug(f"Не указан класс Store в {self.__class__.__name__}")
            # raise AttributeError(f"Не указан класс Store в {self.__class__.__name__}")
        try:
            self.manager = getattr(self.Meta, "manager")
        except AttributeError:
            self.logger.debug(f"Не указан класс Manager в {self.__class__.__name__}")
            # raise AttributeError(f"Не указан класс Manager в {self.__class__.__name__}")
        try:
            self.endpoints = getattr(self.Meta, "endpoints")
        except AttributeError:
            raise AttributeError(
                f"Не указаны данные для построения API {self.__class__.__name__}"
            )

        self.__add_api_route(self.Meta.endpoints)

    def __add_api_route(self, endpoints: EndpointType):
        for func_name, values in endpoints.items():
            if func := values.get(func_name, getattr(self, func_name, None)):
                func.__annotations__.update(values.get("annotations", {}))
                self.add_api_route(
                    methods=values.get("methods", []),
                    path=values["path"] if values.get("path") else "",
                    endpoint=func,
                    summary=values.get("summary", ""),
                    description=values.get("description", ""),
                    response_model=values.get("response_model", None),
                )
            else:
                raise AttributeError(f"Не указан метод {func_name}")

    async def get_all(self, page: int = PAGE, page_size: int = PAGE_SIZE):
        return await self.store.get_all((page - 1) * page_size, page_size)

    async def get_by_id(self, id_: Any):
        return await self.store.get_by_id(id_)

    async def create(self, data: Any):
        return await self.store.create(**data.model_dump())

    async def update(self, data: Any):
        return await self.store.update(**data.model_dump(exclude_none=True))

    async def delete_by_id(self, id_: Any):
        return await self.store.delete_by_id(id_)
