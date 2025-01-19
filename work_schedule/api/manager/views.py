from icecream import ic

from api.base.route import BaseView
from api.manager.schemes import (
    CreateSchema,
    FullDataDriverSchema,
    AssignCarDriverSchema,
    AssignCarDriverCreateSchema,
)
from core.lifespan import db
from store.ws.manager.accessor import ManagerAccessor


class ManagerViews(BaseView):
    db: ManagerAccessor

    class Meta:
        db = db.manager
        endpoints = {
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CreateSchema},
                "response_model": FullDataDriverSchema,
            },
            "create_assign_car_driver": {
                "path": "/assign_car_driver",
                "methods": ["POST"],
                "annotations": {"data": AssignCarDriverCreateSchema},
                "response_model": AssignCarDriverSchema,
            },
        }

    async def create(self, data: CreateSchema) -> FullDataDriverSchema:
        driver, work_schedule_history = await self.db.create(**data.model_dump())
        return FullDataDriverSchema(
            driver=driver.as_dict, work_schedule_history=work_schedule_history.as_dict
        )

    async def create_assign_car_driver(
        self, data: AssignCarDriverCreateSchema
    ) -> AssignCarDriverSchema:
        result = ic(await self.db.assign_car_driver(**data.model_dump()))
        return result
