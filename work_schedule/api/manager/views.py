from icecream import ic

from api.base.route import BaseView
from api.manager.schemes import CreateSchema, FullDataDriverSchema
from core.lifespan import db


class ManagerViews(BaseView):
    class Meta:
        db = db.manager
        endpoints = {
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CreateSchema},
                "response_model": FullDataDriverSchema,
            },
        }

    async def create(self, data: CreateSchema) -> FullDataDriverSchema:
        driver, work_schedule_history = await self.db.create(**data.model_dump())
        return FullDataDriverSchema(driver=driver.as_dict,
                                    work_schedule_history=work_schedule_history.as_dict)
