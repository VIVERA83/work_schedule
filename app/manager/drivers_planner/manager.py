from datetime import datetime

from api.worker_schedule.schemes import CrewSchema
from driver_scheduling.schedule_manager import ScheduleManager
from driver_scheduling.worker_schedule import WorkerSchedule
from excel.excel import Excel
from store.excel.crew_sheet import CrewSheet
from store.excel.dispatchplan import StatisticCalculator
from store.manager.manager import CrewsManager
from manager.base.manager import BaseManager


class DriversPlannerManager(BaseManager):
    async def get_worker_schedule(
        self, id_: int, start_date: datetime, end_date: datetime
    ):
        result = await self.store.drivers_planner.get_current_worker_schedule_by_id(id_)
        return WorkerSchedule(**result).get_schedule(start_date, end_date)

    async def get_all_crews(self, start_date: datetime, end_date: datetime):
        # Получаем список экипажей с графиками работы в указанный диапазон времени
        row_crews = await self.store.drivers_planner.get_crew_schedule(
            start_date, end_date
        )

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
        CrewSheet(static, sheet).fill_in_data_sheet()
        excel.save()
        return crews
