from api.base.route import BaseView
from api.manager.schemes import (
    AddDriverSchema,
    FullDataDriverSchema,
    AddCarSchema,
    FullDataCarSchema,
)
from core.lifespan import store
from store.ws.manager.accessor import ManagerAccessor


class ManagerViews(BaseView):
    db: ManagerAccessor

    class Meta:
        db = store.manager
        endpoints = {
            "add_driver": {
                "path": "/driver",
                "methods": ["POST"],
                "annotations": {"data": AddDriverSchema},
                "response_model": FullDataDriverSchema,
                "summary": "Добавить водителя",
                "description": "Добавить водителя и назначения графика работы.",
            },
            "add_car": {
                "path": "/car",
                "methods": ["POST"],
                "annotations": {"data": AddCarSchema},
                "response_model": FullDataCarSchema,
                "summary": "Добавить машину",
                "description": "Добавить машину и назначения графика работы (проведения `ППО/ППР`).",
            },
            # "create_assign_car_driver": {
            #     "path": "/assign_car_driver",
            #     "methods": ["POST"],
            #     "annotations": {"data": AssignCarDriverCreateSchema},
            #     "response_model": AssignCarDriverSchema,
            #     "summary": "Закрепить водителя за машиной",
            #     "description": "Закрепить водителя за машиной, "
            #     "необходимо помнить что за одной машиной не должно быть закреплено более 3х водителей.",
            # },
        }

    async def add_driver(self, data: AddDriverSchema) -> FullDataDriverSchema:
        driver, work_schedule_history = await self.db.create(**data.model_dump())
        return FullDataDriverSchema(
            driver=driver.as_dict, work_schedule_history=work_schedule_history.as_dict
        )

    async def add_car(self, data: AddCarSchema) -> FullDataCarSchema:
        self.db.logger.debug(
            f"{self.__class__.__name__}.add_car: входящие параметры {data}"
        )
        car, work_schedule_history = await self.db.add_car_set_schedule(
            **data.model_dump()
        )
        return FullDataCarSchema(
            car=car.as_dict, work_schedule_history=work_schedule_history.as_dict
        )

    # async def create_assign_car_driver(
    #     self, data: AssignCarDriverCreateSchema
    # ) -> AssignCarDriverSchema:
    #     result = await self.db.assign_car_driver(**data.model_dump())
    #     return result
