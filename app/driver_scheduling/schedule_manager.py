from collections import defaultdict
from datetime import datetime

from icecream import ic

from driver_scheduling.combined_employees_work_plan import (
    CombinedEmployeesWorkPlan,
)
from driver_scheduling.utils import DATE, SIGN


class ScheduleManager:
    __combined_employees_work_plans: dict[str, CombinedEmployeesWorkPlan]

    def __init__(self):
        self.__combined_employees_work_plans = {}

    def get_schedule(
        self, start: datetime = datetime.now(), end: datetime = datetime.now()
    ) -> dict[DATE, SIGN]:
        """Возвращает расписание сотрудников."""
        total_plan = defaultdict(dict)
        for plan in self.__combined_employees_work_plans.values():

            for date, employee in plan.get_schedule(start, end).items():
                ic(date, employee)
                total_plan[date].update(**employee)
        ic(total_plan)
        return total_plan

    def add_combined_employees_work_plan(
        self, employee: "CombinedEmployeesWorkPlan"
    ) -> None:
        """Добавить объединенный график работы сотрудников."""
        self.__combined_employees_work_plans[employee.name] = employee
