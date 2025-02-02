from collections import defaultdict
from datetime import datetime
from typing import Generator, Union

from store.scheduler.worker_schedule import Worker, WorkerSchedule
from work_schedule.store.scheduler.utils import DATE, SIGN, SIGNAL_WORK


class EmployeeWorkPlan:
    """План работы сотрудников, на закрепленном оборудовании."""

    __employee_work_plan: dict[DATE, SIGN]
    __unused_employees: dict[DATE, dict[str, SIGNAL_WORK]]

    def __init__(
        self,
        main_worker: Union["Worker", "WorkerSchedule"],
        *workers: Union["Worker", "WorkerSchedule"],
    ):
        """
        :param main_worker: Рабочее расписание некого оборудования или основного сотрудника,
        на цикле работы которого формируется план. Как пример использования можно посмотреть
        вариант построения работы экипажа машины. В main_worker_schedule можно указать
        дни в которые оборудование, будет находиться на техническом обслуживании.
        :param workers: Рабочее расписание сотрудников.
        """
        self.__main_worker_schedule = main_worker
        self.__workers_schedules = workers

    @property
    def name(self) -> str:
        return self.__main_worker_schedule.name

    def get_schedule(
        self, start: datetime = datetime.now(), end: datetime = datetime.now()
    ) -> dict[DATE, SIGN]:
        """Возвращает расписание работы сотрудников."""
        self.__create_employee_work_plan(start, end)
        return self.__employee_work_plan

    def get_unused_employees(
        self, start: datetime = datetime.now(), end: datetime = datetime.now()
    ) -> dict[DATE, dict[str, SIGNAL_WORK]]:
        """Возвращает сотрудников, которые не были задействованы в работе."""
        self.__create_employee_work_plan(start, end)
        return self.__unused_employees

    def __create_employee_work_plan(self, start: datetime, end: datetime):
        """Формирует план работы сотрудников."""
        self.__employee_work_plan = {}
        self.__unused_employees = defaultdict(dict)
        # Если нет циклов работы сотрудников, то формируется план работы оборудования
        if not self.__workers_schedules:
            self.__employee_work_plan = self.__main_worker_schedule.get_schedule(
                start, end
            )
            return

        works_schedules_gens = self._make_schedule_generators(start, end)
        main_worker_schedule_gen = self.__main_worker_schedule.get_schedule_generator(
            start, end
        )
        current_worker_id = self.__workers_schedules[0].name
        date = start.strftime(self.__main_worker_schedule.date_format)
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

                            ins = {
                                list(works_schedules_gens.keys()).index(id_): [id_, s]
                                for id_, s in buffer_data.items()
                            }

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

    def _make_schedule_generators(
        self, start: datetime = datetime.now(), end: datetime = datetime.now()
    ) -> dict[str, Generator[tuple[DATE, SIGN], DATE, None]]:
        """Генератор расписания работы сотрудников."""
        return {
            schedule.name: schedule.get_schedule_generator(start, end)
            for schedule in self.__workers_schedules
        }
