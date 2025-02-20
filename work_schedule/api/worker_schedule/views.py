from collections import defaultdict
from datetime import datetime

from icecream import ic

from api.base.route import BaseView
from api.worker_schedule.schemes import (
    WorkerScheduleCreateSchema,
    WorkerScheduleSchema,
    CrewSchema,
    ScheduleHistorySchema,
)
from api.worker_schedule.utils import create_worker
from core.lifespan import store
from store.excel.excel import Excel
from store.excel.utils import black_fill, orange_fill, red_fill, green_fill
from store.scheduler.combined_employees_work_plan import CombinedEmployeesWorkPlan
from store.scheduler.employee_work_plan import EmployeeWorkPlan
from store.scheduler.schedule_manager import ScheduleManager
from store.scheduler.utils import SIGNAL_WORK, SIGNAL_WEEKEND

from store.store import Store
from test_area.crew.temp import CrewsManager
from test_area.exel_1.excel import CrewExel
from test_area.exel_1.statistic import StatisticCalculator


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
        CrewExel(excel, static).create()
        excel.auto_alignment_column_center()
        excel.auto_alignment_column_width()
        excel.save()
        return crews
