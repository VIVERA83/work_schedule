from collections import defaultdict

from work_schedule.store.scheduler.employee_work_plan import EmployeeWorkPlan
from work_schedule.store.scheduler.utils import DATE, SIGN, SIGNAL_WORK, SIGNAL_WEEKEND


class CombinedEmployeesWorkPlan:
    __employee_work_plan: dict[DATE, SIGN]
    __unused_employees: dict[DATE, dict[str, SIGNAL_WORK]]

    def __init__(self, employee_1: EmployeeWorkPlan, employee_2: EmployeeWorkPlan):
        self.employee_1 = employee_1
        self.employee_2 = employee_2
        self.__merge_employee_work_plan()

    def get_employee_work_plan(self) -> dict[DATE, SIGN]:
        """Возвращает план работы сотрудников."""
        return self.__employee_work_plan

    def get_unused_employees(self) -> dict[DATE, dict[str, SIGNAL_WORK]]:
        """Возвращает сотрудников, которые не были задействованы в работе."""
        return self.__unused_employees

    def __merge_employee_work_plan(self):
        self.__employee_work_plan = defaultdict(dict)
        self.__merge_unused_employees()

        for (date_1, name_1), (date_2, name_2) in zip(self.employee_1.get_employee_work_plan().items(),
                                                      self.employee_2.get_employee_work_plan().items()):

            if name_1 != name_2:
                temp = {}
                # 1
                if name_1 in [SIGNAL_WEEKEND]:
                    if today_unused := list(self.__unused_employees.get(date_1).keys()):
                        new_worker = today_unused[0]
                        temp.update({
                            self.employee_1.name: name_1,
                            self.employee_2.name: new_worker
                        })
                        self.__unused_employees.get(date_1).pop(new_worker)
                    else:
                        temp.update({self.employee_2.name: name_2})
                else:
                    temp = {
                        self.employee_1.name: name_1,
                        self.employee_2.name: name_2,
                    }
                self.__employee_work_plan[date_1].update(temp)


            else:
                if name_1 in [SIGNAL_WEEKEND] and name_2 in [SIGNAL_WEEKEND]:
                    self.__employee_work_plan[date_1] = {
                        self.employee_1.name: name_1,
                        self.employee_2.name: name_2,
                    }
                else:
                    if data := list(self.__unused_employees.pop(date_1, {}).keys()):
                        self.__employee_work_plan[date_1] = {
                            self.employee_1.name: name_1,
                            self.employee_2.name: data[-1],
                        }
                    else:
                        self.__employee_work_plan[date_1] = {
                            self.employee_1.name: name_1,
                            self.employee_2.name: SIGNAL_WORK,
                        }

            # удаление повторов
            self.__removing_duplicates_from_unused(date_1)

    def __merge_unused_employees(self):
        self.__unused_employees = {
            date_1: {**values_1, **values_2}
            for (date_1, values_1), (date_2, values_2), in zip(self.employee_1.get_unused_employees().items(),
                                                               self.employee_2.get_unused_employees().items(),
                                                               )

        }

    def __removing_duplicates_from_unused(self, date: str):
        if data := self.__unused_employees.get(date):
            a = set(self.__employee_work_plan[date].values())
            b = set(data.keys())
            if c := b - a:
                self.__unused_employees[date] = {
                    element: self.__unused_employees[date][element]
                    for element in c
                }
            elif a == b:
                self.__unused_employees[date] = {
                    element: self.__unused_employees[date][element]
                    for element in c
                }
            if not self.__unused_employees[date]:
                del self.__unused_employees[date]
