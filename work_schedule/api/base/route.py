from typing import Any

from fastapi import APIRouter

from store.ws.base.accessor import BaseAccessor


class BaseRoute(APIRouter):
    def __init__(
        self, prefix: str, tags: list[str], db: BaseAccessor, endpoints: dict[str, Any]
    ):
        super().__init__(prefix=prefix, tags=tags)
        self.db = db
        self.__add_api_route(endpoints)

    def __add_api_route(self, endpoints: dict[str, Any]):
        for endpoint, values in endpoints.items():
            if func := values.get(endpoint, getattr(self, endpoint, None)):  # noqa
                func.__annotations__.update(values.get("annotations", {}))  # noqa
                self.add_api_route(
                    methods=values.get("methods", []),
                    path=values["path"] if values.get("path") else "",
                    endpoint=func,
                    summary=values.get("summary", ""),
                    description=values.get("description", ""),
                    response_model=values.get("response_model", None),
                )

    async def get_by_id(self, id_: Any):
        return await self.db.get_by_id(id_)

    async def create(self, data: Any):
        return await self.db.create(**data.model_dump())

    async def update(self, data: Any):
        return await self.db.create(**data.model_dump())

    async def delete_by_id(self, id_: Any):
        return await self.db.delete_by_id(id_)
