from collections import defaultdict
from datetime import datetime
from typing import Generator

from work_schedule.store.scheduler.schedule_maker import WorkerSchedule
from work_schedule.store.scheduler.utils import DATE, SIGN, SIGNAL_WORK


class EmployeeWorkPlan:
    """План работы сотрудников, на закрепленном оборудовании."""

    __employee_work_plan: dict[DATE, SIGN]
    __unused_employees: dict[DATE, dict[str, SIGNAL_WORK]]

    def __init__(self,
                 start: datetime,
                 end: datetime,
                 main_worker_schedule: "WorkerSchedule",
                 *worker_schedule: "WorkerSchedule"
                 ):
        """
        :param start: Дата начала цикла работы.
        :param end: Дата окончания цикла работы.
        :param main_worker_schedule: Рабочее расписание некого оборудования или основного сотрудника,
        на цикле работы которого формируется план. Как пример использования можно посмотреть
        вариант построения работы экипажа машины. В main_worker_schedule можно указать
        дни в которые оборудование, будет находиться на техническом обслуживании.
        :param worker_schedule: Рабочее расписание сотрудников.
        """
        self.__start = start
        self.__end = end
        self.__main_worker_schedule = main_worker_schedule
        self.__workers_schedules = worker_schedule
        self.__create_employee_work_plan()

    @property
    def name(self) -> str:
        return self.__main_worker_schedule.name

    def get_employee_work_plan(self) -> dict[DATE, SIGN]:
        """Возвращает план работы сотрудников."""
        return self.__employee_work_plan

    def get_unused_employees(self) -> dict[DATE, dict[str, SIGNAL_WORK]]:
        """Возвращает сотрудников, которые не были задействованы в работе."""
        return self.__unused_employees

    def __create_employee_work_plan(self):
        """Формирует план работы сотрудников."""
        self.__employee_work_plan = {}
        self.__unused_employees = defaultdict(dict)
        if not self.__workers_schedules:
            self.__employee_work_plan = self.__main_worker_schedule.make_schedule(self.__start, self.__end)
            return

        works_schedules_gens = self._make_schedule_generators()
        main_worker_schedule_gen = self.__main_worker_schedule.make_schedule_generator(self.__start, self.__end)
        current_worker_id = self.__workers_schedules[0].name
        date = self.__start.strftime(self.__main_worker_schedule.date_format)
        current_worker_index = 0

        while True:
            try:
                car_date, main_signal = next(main_worker_schedule_gen)
                if main_signal == SIGNAL_WORK:

                    for index, (id_, gen) in enumerate(works_schedules_gens.items()):
                        date, signal = next(gen)

                        if current_worker_id == id_ and signal == SIGNAL_WORK:
                            self.__employee_work_plan[date] = current_worker_id
                            current_worker_index = index
                        elif signal == SIGNAL_WORK:
                            self.__unused_employees[date][id_] = signal

                    if self.__employee_work_plan.get(date, None) is None:
                        if buffer_data := self.__unused_employees.get(date, None):

                            ins = {list(works_schedules_gens.keys()).index(id_): [id_, s] for id_, s in
                                   buffer_data.items()}

                            for ind, (id_, s) in ins.items():

                                if ind > current_worker_index:
                                    current_worker_id = id_
                                    break

                            if buffer_data.get(current_worker_id, None) is None:
                                current_worker_id = ins[list(ins.keys())[0]][0]
                            buffer_data.pop(current_worker_id)
                            self.__employee_work_plan[date] = current_worker_id

                            if not self.__unused_employees.get(date, None):
                                self.__unused_employees.pop(date)

                        else:
                            self.__employee_work_plan[car_date] = main_signal
                else:
                    self.__employee_work_plan[car_date] = main_signal
                    for index, (id_, gen) in enumerate(works_schedules_gens.items()):
                        date, signal = next(gen)
                        if signal == SIGNAL_WORK:
                            self.__unused_employees[date][id_] = signal
            except StopIteration:
                break

    def _make_schedule_generators(self) -> dict[str, Generator[
        tuple[DATE, SIGN], DATE, None]]:
        """Генератор расписания работы сотрудников."""
        return {
            schedule.name: schedule.make_schedule_generator(self.__start, self.__end)
            for schedule in
            self.__workers_schedules
        }
