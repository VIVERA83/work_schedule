from datetime import datetime

from icecream import ic

from store.scheduler.employee_work_plan import EmployeeWorkPlan
from store.scheduler.worker_schedule import Worker, WorkerSchedule

# class Worker:
#     """Работник."""
#
#     __worker_schedules: dict[datetime, WorkerSchedule]
#
#     def __init__(
#         self,
#         name: str,
#         schedule_start_date: datetime,
#         work_days: int,
#         weekend_days: int,
#         is_working: bool,
#         what_day: int,
#         date_format: str = DATE_FORMAT,
#     ):
#         self.name = name
#         self.date_format = date_format
#         self.__worker_schedules = {
#             schedule_start_date: WorkerSchedule(
#                 name=name,
#                 schedule_start_date=schedule_start_date,
#                 work_days=work_days,
#                 weekend_days=weekend_days,
#                 is_working=is_working,
#                 what_day=what_day,
#                 date_format=date_format,
#             )
#         }
#
#     def add_worker_schedule(
#         self,
#         schedule_start_date: datetime,
#         work_days: int,
#         weekend_days: int,
#         is_working: bool,
#         what_day: int,
#     ):
#         """Добавить рабочее расписание.
#
#         Требуется для корректного построения итогового расписания если
#         в запрашиваемый период происходит смена графика работы.
#         """
#         self.__worker_schedules[schedule_start_date] = WorkerSchedule(
#             name=self.name,
#             schedule_start_date=schedule_start_date,
#             work_days=work_days,
#             weekend_days=weekend_days,
#             is_working=is_working,
#             what_day=what_day,
#             date_format=self.date_format,
#         )
#         self.__worker_schedules = {
#             date: self.__worker_schedules[date]
#             for date in sorted(list(self.__worker_schedules.keys()))
#         }
#
#     def get_schedule(
#         self, start_date: datetime, end_date: datetime
#     ) -> dict[DATE, SIGN]:
#         """Получить расписание.
#
#         Выдается расписание с учетом изменений в графике работы.
#
#         :param start_date: Дата начала период.
#         :param end_date: Дата окончания период.
#         :return: Словарь с расписанием, где ключ - дата (строковое представление даты),
#          значение - одно из сигналов (строковое представление сигнала).
#         """
#         schedule = {}
#         schedule_dates = self.get_closest_dates(start_date, end_date)
#         while schedule_dates:
#             date = schedule_dates.pop(0)
#             if schedule_dates:
#                 next_date = schedule_dates[0]
#             else:
#                 next_date = end_date
#             schedule.update(
#                 self.__worker_schedules[date].make_schedule(start_date, next_date)
#             )
#             start_date = next_date
#         return schedule
#
#     def get_closest_dates(
#         self, start_date: datetime, end_date: datetime
#     ) -> list[datetime]:
#         """Получить список дат, изменений в расписании.
#
#         :param start_date: Дата начала период.
#         :param end_date: Дата окончания период.
#         :return: Список дат, изменений в расписании.
#         """
#
#         min_date = [list(self.__worker_schedules.keys())[0]]
#         for date in self.__worker_schedules.keys():
#             if start_date >= date:
#                 min_date = [date]
#
#         for date in self.__worker_schedules.keys():
#             if min_date[-1] != date and min_date[-1] <= date <= end_date:
#                 min_date.append(date)
#         return min_date


if __name__ == "__main__":
    date_2025_01_01 = datetime(2025, 1, 1)
    date_2025_01_10 = datetime(2025, 1, 10)
    date_2025_01_17 = datetime(2025, 1, 17)
    date_2025_01_18 = datetime(2025, 1, 18)
    date_2025_01_20 = datetime(2025, 1, 20)
    date_2025_01_21 = datetime(2025, 1, 21)
    # два работника
    worker_1 = Worker("Яшин Александр Кириллович", date_2025_01_10, 4, 4, True, 3)
    worker_2 = Worker('Миронов Михаил Викторович', date_2025_01_10, 2,  2,  True, 2,)
    # добавляем некие смены графиков работы
    worker_1.add_worker_schedule(date_2025_01_17, 4, 2, False, 1)
    worker_1.add_worker_schedule(date_2025_01_20, 4, 2, False, 1)
    ic(worker_1.get_schedule(date_2025_01_10, date_2025_01_21))

    for data in worker_1.get_schedule_generator(date_2025_01_10, date_2025_01_21):
        print(data)
    # машина
    car = WorkerSchedule("CAR_1", date_2025_01_01, work_days=-1, weekend_days=-1, is_working=True, what_day=1)
    # закрепляем на машину двух водителей которые работают на этой машине согласно своему графику работы
    employee_work_plan = EmployeeWorkPlan(car, worker_1, worker_2)
    ic(employee_work_plan.get_schedule(date_2025_01_10, date_2025_01_21))
    # нужно найти машины, которые входят в экипаж.

