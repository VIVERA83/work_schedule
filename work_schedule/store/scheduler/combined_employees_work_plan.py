from collections import defaultdict
from datetime import datetime

from icecream import ic

from work_schedule.store.scheduler.employee_work_plan import EmployeeWorkPlan
from work_schedule.store.scheduler.utils import DATE, SIGN, SIGNAL_WEEKEND, SIGNAL_WORK


# ver 2.0
class CombinedEmployeesWorkPlan:
    """Объединенный график работы сотрудников на оборудовании."""

    # то есть закрепленные экипажи, которые работают на указанных машинах
    __employee_work_plan: dict[DATE, SIGN]
    __unused_employees: dict[DATE, dict[str, SIGNAL_WORK]]

    def __init__(self, employee_1: EmployeeWorkPlan, employee_2: EmployeeWorkPlan = None):
        ic(employee_1, employee_2)
        self.name = f"{employee_1.name}"
        self.employee_1 = employee_1
        self.employee_2 = employee_2
        if self.employee_2:
            self.name += " + " + self.employee_2.name

    def get_schedule(self, start: datetime, end: datetime) -> dict[DATE, SIGN]:
        """Возвращает расписание работы сотрудников."""
        if self.employee_2:
            self.__create_employee_work_plan(start, end)
        else:
            ic(self.employee_1)
            self.__create_employee_work_plan_2(start, end)
            ic(self.__employee_work_plan)
        return self.__employee_work_plan

    def get_unused_employees(self, start: datetime, end: datetime) -> dict[DATE, dict[str, SIGNAL_WORK]]:
        """Возвращает сотрудников, которые не были задействованы в работе."""
        if self.employee_2:
            self.__create_employee_work_plan(start, end)
        else:
            self.__create_employee_work_plan_2(start, end)
            ic(self.__unused_employees)
        return self.__unused_employees

    def __create_employee_work_plan(self, start: datetime, end: datetime):
        self.__employee_work_plan = defaultdict(dict)
        self.__merge_unused_employees(start, end)

        for (date_1, name_1), (_, name_2) in self.__zip_employees_schedule(start, end):
            temp = {self.employee_1.name: name_1}
            if name_1 != name_2:
                if name_1 in [SIGNAL_WEEKEND]:
                    if today_unused := list(self.__unused_employees.get(date_1).keys()):
                        temp[self.employee_2.name] = today_unused[0]
                    else:
                        temp = {self.employee_2.name: name_2}
                else:
                    temp[self.employee_2.name] = name_2

            else:
                if name_1 in [SIGNAL_WEEKEND] and name_2 in [SIGNAL_WEEKEND]:
                    temp.update({self.employee_2.name: name_2})
                else:
                    if data := list(self.__unused_employees.get(date_1, {}).keys()):
                        temp.update({self.employee_2.name: data[-1]})
                    else:
                        temp.update({self.employee_2.name: SIGNAL_WORK})
            self.__employee_work_plan[date_1].update(temp)

            # удаление повторов
            self.__removing_duplicates_from_unused(date_1)

    def __merge_unused_employees(self, start: datetime, end: datetime):
        self.__unused_employees = {
            date_1: {**values_1, **values_2}
            for (date_1, values_1), (date_2, values_2) in zip(
                self.employee_1.get_unused_employees(start, end).items(),
                self.employee_2.get_unused_employees(start, end).items(),
            )
        }

    def __removing_duplicates_from_unused(self, date: str):
        if data := self.__unused_employees.get(date):
            a = set(self.__employee_work_plan[date].values())
            b = set(data.keys())
            for element in a:
                if element in b:
                    del data[element]
            if not self.__unused_employees[date]:
                del self.__unused_employees[date]

    def __zip_employees_schedule(self, start: datetime, end: datetime) -> zip:
        return zip(
            self.employee_1.get_schedule(start, end).items(),
            self.employee_2.get_schedule(start, end).items(),
        )

    def __create_employee_work_plan_2(self, start: datetime, end: datetime):
        self.__employee_work_plan = defaultdict(dict)

        self.__unused_employees = {}
        for date_1, values_1 in self.employee_1.get_unused_employees(start, end).items():
            self.__unused_employees[date_1] = {**values_1}

        for date_1, name_1 in self.employee_1.get_schedule(start, end).items():
            temp = {self.employee_1.name: name_1}
            self.__employee_work_plan[date_1].update(temp)

    def __str__(self):
        return f"{self.__class__.__name__} {self.name}"

    __repr__ = __str__

# # ver 1.0
# class CombinedEmployeesWorkPlan:
#     """Объединенный график работы сотрудников на оборудовании."""
#
#     # то есть закрепленные экипажи, которые работают на указанных машинах
#     __employee_work_plan: dict[DATE, SIGN]
#     __unused_employees: dict[DATE, dict[str, SIGNAL_WORK]]
#
#     def __init__(self, employee_1: EmployeeWorkPlan, employee_2: EmployeeWorkPlan):
#         self.name = f"{employee_1.name} + {employee_2.name}"
#         self.employee_1 = employee_1
#         self.employee_2 = employee_2
#
#     def get_schedule(
#         self, start: datetime = datetime.now(), end: datetime = datetime.now()
#     ) -> dict[DATE, SIGN]:
#         """Возвращает расписание работы сотрудников."""
#         self.__create_employee_work_plan(start, end)
#         return self.__employee_work_plan
#
#     def get_unused_employees(self) -> dict[DATE, dict[str, SIGNAL_WORK]]:
#         """Возвращает сотрудников, которые не были задействованы в работе."""
#         return self.__unused_employees
#
#     def __create_employee_work_plan(self, start: datetime, end: datetime):
#         self.__employee_work_plan = defaultdict(dict)
#         self.__merge_unused_employees(start, end)
#
#         for (date_1, name_1), (_, name_2) in zip(
#             self.employee_1.get_schedule(start, end).items(),
#             self.employee_2.get_schedule(start, end).items(),
#         ):
#             temp = {self.employee_1.name: name_1}
#             if name_1 != name_2:
#                 if name_1 in [SIGNAL_WEEKEND]:
#                     if today_unused := list(self.__unused_employees.get(date_1).keys()):
#                         temp[self.employee_2.name] = today_unused[0]
#                     else:
#                         temp = {self.employee_2.name: name_2}
#                 else:
#                     temp[self.employee_2.name] = name_2
#
#             else:
#                 if name_1 in [SIGNAL_WEEKEND] and name_2 in [SIGNAL_WEEKEND]:
#                     temp.update({self.employee_2.name: name_2})
#                 else:
#                     if data := list(self.__unused_employees.get(date_1, {}).keys()):
#                         temp.update({self.employee_2.name: data[-1]})
#                     else:
#                         temp.update({self.employee_2.name: SIGNAL_WORK})
#             self.__employee_work_plan[date_1].update(temp)
#
#             # удаление повторов
#             self.__removing_duplicates_from_unused(date_1)
#
#     def __merge_unused_employees(self, start: datetime, end: datetime):
#         self.__unused_employees = {
#             date_1: {**values_1, **values_2}
#             for (date_1, values_1), (date_2, values_2) in zip(
#                 self.employee_1.get_unused_employees(start, end).items(),
#                 self.employee_2.get_unused_employees(start, end).items(),
#             )
#         }
#
#     def __removing_duplicates_from_unused(self, date: str):
#         if data := self.__unused_employees.get(date):
#             a = set(self.__employee_work_plan[date].values())
#             b = set(data.keys())
#             for element in a:
#                 if element in b:
#                     del data[element]
#             if not self.__unused_employees[date]:
#                 del self.__unused_employees[date]
#
#     def __str__(self):
#         return f"{self.__class__.__name__} {self.name}"
#
#     __repr__ = __str__
