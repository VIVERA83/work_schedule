from datetime import datetime

from api.base.route import BaseView
from api.worker_schedule.schemes import (
    WorkerScheduleCreateSchema,
    WorkerScheduleSchema,
    CrewSchema,
)
from core.lifespan import store
from store.store import Store


class WorkerScheduleViews(BaseView):
    db: Store

    class Meta:
        db = store
        endpoints = {
            "get_worker_schedule": {
                "methods": ["POST"],
                "annotations": {"data": WorkerScheduleCreateSchema},
                "response_model": WorkerScheduleSchema,
                "path": "/get_driver_schedule",
                "summary": "Получить график водителя",
                "description": "получение данных для построения графика графика работы водителя.",
            },
            "get_all_crews": {
                "methods": ["GET"],
                "path": "/get_all_crews",
                "response_model": list[CrewSchema],
                "summary": "Получить список экипажей",
                "description": "Получить список экипажей с графиками работы в указанный диапазон времени",
            },
        }

    async def get_worker_schedule(self, data: WorkerScheduleCreateSchema):
        return await self.db.manage_worker_schedule.get_worker_schedule(
            **data.model_dump()
        )

    async def get_all_crews(
        self,
        start_date: datetime = datetime.now(),
        end_date: datetime = datetime.now(),
    ):
        row_crews = await self.db.manager.get_all_crews(start_date, end_date)
        return [
            CrewSchema(id=item[0], cars=item[1], drivers=item[2]) for item in row_crews
        ]
