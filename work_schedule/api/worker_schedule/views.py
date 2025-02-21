from datetime import datetime

from api.base.route import BaseView
from api.worker_schedule.schemes import (
    WorkerScheduleCreateSchema,
    WorkerScheduleSchema,
    CrewSchema,
)

from core.lifespan import store
from excel.excel import Excel
from store.excel.crew_excel import CrewSheet
from store.excel.statistic import StatisticCalculator
from store.manager.manager import CrewsManager

from driver_scheduling.schedule_manager import ScheduleManager


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

    async def get_all_crews(self, start_date: datetime, end_date: datetime):
        # Получаем список экипажей с графиками работы в указанный диапазон времени
        row_crews = await self.db.manager.get_all_crews(start_date, end_date)

        # Преобразовали список в словарь экипажей, ключ = id экипажа, моделей Pydantic
        dict_crews = {
            item[0]: CrewSchema(id=item[0], cars=item[1], drivers=item[2])
            for item in row_crews
        }

        # теперь экипажи преобразовать в CombinedEmployeesWorkPlan (Объединенный график работы сотрудников на оборудовании.)
        combined_employees_work_plans = CrewsManager(dict_crews, start_date, end_date)()

        crews = [
            CrewSchema(id=item[0], cars=item[1], drivers=item[2]) for item in row_crews
        ]

        # теперь все засунуть в excel
        excel = Excel("test.xlsx")
        manager = ScheduleManager()
        for combined_employees_work_plan in combined_employees_work_plans.values():
            manager.add_combined_employees_work_plan(combined_employees_work_plan)
        data = manager.get_schedule(start_date, end_date)
        static = StatisticCalculator(data)
        sheet = excel.create_sheet("График работы")
        CrewSheet(static,sheet).fill_in_data_sheet()
        excel.save()
        return crews
