import os
from datetime import datetime

from starlette.background import BackgroundTask
from starlette.responses import FileResponse

from api.base.route import BaseView
from api.worker_schedule.schemes import (
    WorkerScheduleCreateSchema,
    WorkerScheduleSchema,
    START_DATE,
    END_DATE,
)
from api.worker_schedule.utils import delete_file

from core.lifespan import manager


class WorkerScheduleViews(BaseView):
    class Meta:
        manager = manager
        endpoints = {
            "get_worker_schedule": {
                "methods": ["POST"],
                "path": "/get_driver_schedule",
                "annotations": {"data": WorkerScheduleCreateSchema},
                "response_model": WorkerScheduleSchema,
                "summary": "Получить график водителя",
                "description": "получение данных для построения графика графика работы водителя.",
            },
            "download_excel_file_driver_schedule": {
                "methods": ["GET"],
                "path": "/download_excel_file_driver_schedule",
                "summary": "Скачать наряд в excel файле",
                "description": "Скачать наряд в excel файле, за указанный период.",
            },
        }

    async def get_worker_schedule(self, data: WorkerScheduleCreateSchema):
        return await self.manager.drivers_planner.get_schedule(**data.model_dump())

    async def download_excel_file_driver_schedule(
        self, start_date: datetime = START_DATE, end_date: datetime = END_DATE
    ):
        path_to_file = (
            await self.manager.drivers_planner.export_driver_schedule_to_excel(
                start_date, end_date
            )
        )
        return FileResponse(
            path_to_file,
            filename=os.path.basename(path_to_file),
            background=BackgroundTask(delete_file, path_to_file, self.logger),
            headers={
                "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            },
        )
