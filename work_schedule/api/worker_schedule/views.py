from datetime import datetime

from icecream import ic

from api.base.route import BaseView
from api.worker_schedule.schemes import WorkerScheduleCreateSchema, WorkerScheduleSchema
from core.lifespan import store
from store.scheduler.employee_work_plan import EmployeeWorkPlan
from store.scheduler.worker_schedule import WorkerSchedule
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
            "get_schedule": {
                "methods": ["GET"],
                "path": "/get_schedule",
            },
        }

    async def get_worker_schedule(self, data: WorkerScheduleCreateSchema):
        return await self.db.manage_worker_schedule.get_worker_schedule(
            **data.model_dump()
        )

    async def get_schedule(
        self,
        car_id: int,
        start_date: datetime = datetime.now(),
        end_date: datetime = datetime.now(),
    ):
        result = await self.db.manager.get_all_bak(car_id, start_date, end_date)

        date_string = "2025-01-21T00:00:00"
        date_format = "%Y-%m-%dT%H:%M:%S"

        date_object = datetime.strptime(date_string, date_format)

        for data in result:
            for d in data:
                ic(d)
        return "ok"
