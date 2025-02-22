from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Generator, ParamSpec, TypeVar

from driver_scheduling.utils import (
    DATE,
    DATE_FORMAT,
    SIGN,
    generator_timetable_period,
    get_timetable_period,
    validate_make_date,
)

_PWrapped = ParamSpec("_PWrapped")
_RWrapped = TypeVar("_RWrapped")


class WorkerSchedule:
    """График работы."""

    def __init__(
        self,
        name: str,
        schedule_start_date: datetime,
        work_days: int,
        weekend_days: int,
        is_working: bool,
        what_day: int,
        date_format: str = DATE_FORMAT,
    ):
        self.name = name
        self.schedule_start_date = schedule_start_date
        self.work_days = work_days
        self.weekend_days = weekend_days
        self.is_working = is_working
        self.what_day = what_day
        self.date_format = date_format

    def __check_make_data(
        self: Callable[_PWrapped, _RWrapped],
    ) -> Callable[_PWrapped, _RWrapped]:
        """Проверка корректности введенных дат."""

        @wraps(self)
        def wrapper(cls, start_date: datetime, end_date: datetime, *args, **kwargs):
            """Проверка корректности введенных дат.

            Дата начало периода должна быть в границах даты начала расписания и даты окончания периода
            Дата окончания периода должна быть в границах даты начала расписания и даты окончания периода.
            При не соответствии корректности введенных дат генерируется исключение ValueError.

            :param cls: - Материнский экземпляр класса.
            :param start_date: Дата начала период.
            :param end_date: Дата окончания период.

            """
            # validate_make_date(cls.schedule_start_date, start_date, end_date)
            validate_make_date( start_date, end_date)
            return self(cls, start_date, end_date, *args, **kwargs)

        return wrapper

    @__check_make_data  # noqa
    def get_schedule(
        self, start_date: datetime, end_date: datetime
    ) -> dict[DATE, SIGN]:
        """Создание расписания по датам.

        :param start_date: Дата начала период.
        :param end_date: Дата окончания период.
        :return: Словарь с расписанием, где ключ - дата (строковое представление даты),
         значение - одно из сигналов (строковое представление сигнала).
        """
        return get_timetable_period(
            schedule_start_date=self.schedule_start_date,
            work_days=self.work_days,
            weekend_days=self.weekend_days,
            is_working=self.is_working,
            what_day=self.what_day,
            start_date=start_date,
            end_date=end_date,
            date_format=self.date_format,
        )

    @__check_make_data  # noqa
    def get_schedule_generator(
        self, start_date: datetime, end_date: datetime
    ) -> Generator[tuple[DATE, SIGN], DATE, None]:
        """Генератор расписания по датам.

        Генератор принимает дату next_date (строка) - пропускает выдачу следующих данных до указанной даты.

        :param start_date: Дата начала период.
        :param end_date: Дата окончания период.
        :return: Генератор с расписанием, где первый элемент - дата (строковое представление даты),

         второй элемент - один из сигналов (строковое представление сигнала).
        """
        gen = generator_timetable_period(
            schedule_start_date=self.schedule_start_date,
            work_days=self.work_days,
            weekend_days=self.weekend_days,
            is_working=self.is_working,
            what_day=self.what_day,
            start_date=start_date,
            end_date=end_date,
            date_format=self.date_format,
        )
        next_date = None
        buffer = None
        for date, signal in gen:
            if next_date is not None:
                buffer = next_date
            if buffer is not None and datetime.strptime(
                buffer, self.date_format
            ) > datetime.strptime(date, self.date_format):
                continue
            next_date = yield date, signal

    def __repr__(self) -> str:
        return f"WorkerSchedule(name={self.name}, schedule_start_date={self.schedule_start_date}, work_days={self.work_days}, weekend_days={self.weekend_days}, is_working={self.is_working}, what_day={self.what_day}, date_format={self.date_format})"


class Worker:
    """Работник.

    Работник имеет имя, дату начала расписания, график работы.
    """

    __worker_schedules: dict[datetime, WorkerSchedule]

    def __init__(
        self,
        name: str,
        schedule_start_date: datetime,
        work_days: int,
        weekend_days: int,
        is_working: bool,
        what_day: int,
        date_format: str = DATE_FORMAT,
    ):
        self.schedule_start_date = schedule_start_date
        self.name = name
        self.date_format = date_format
        self.__worker_schedules = {
            schedule_start_date: WorkerSchedule(
                name=name,
                schedule_start_date=schedule_start_date,
                work_days=work_days,
                weekend_days=weekend_days,
                is_working=is_working,
                what_day=what_day,
                date_format=date_format,
            )
        }

    def add_worker_schedule(
        self,
        schedule_start_date: datetime,
        work_days: int,
        weekend_days: int,
        is_working: bool,
        what_day: int,
    ):
        """Добавить рабочее расписание.

        Требуется для корректного построения итогового расписания если
        в запрашиваемый период происходит смена графика работы.
        """
        self.__worker_schedules[schedule_start_date] = WorkerSchedule(
            name=self.name,
            schedule_start_date=schedule_start_date,
            work_days=work_days,
            weekend_days=weekend_days,
            is_working=is_working,
            what_day=what_day,
            date_format=self.date_format,
        )
        self.__worker_schedules = {
            date: self.__worker_schedules[date]
            for date in sorted(list(self.__worker_schedules.keys()))
        }

    def get_schedule(
        self, start_date: datetime, end_date: datetime
    ) -> dict[DATE, SIGN]:
        """Получить расписание.

        Выдается расписание с учетом изменений в графике работы.

        :param start_date: Дата начала период.
        :param end_date: Дата окончания период.
        :return: Словарь с расписанием, где ключ - дата (строковое представление даты),
         значение - одно из сигналов (строковое представление сигнала).
        """
        schedule = {}
        schedule_dates = self.get_closest_dates(start_date, end_date)
        while schedule_dates:
            date = schedule_dates.pop(0)
            if schedule_dates:
                next_date = schedule_dates[0]
            else:
                next_date = end_date
            schedule.update(
                self.__worker_schedules[date].get_schedule(start_date, next_date)
            )
            start_date = next_date
        return schedule

    def get_schedule_generator(
        self, start_date: datetime, end_date: datetime
    ) -> Generator[tuple[DATE, SIGN], DATE, None]:
        """Генератор расписания по датам."""

        schedule_dates = self.get_closest_dates(start_date, end_date)
        while schedule_dates:
            date = schedule_dates.pop(0)
            if schedule_dates:
                next_date = schedule_dates[0]
            else:
                next_date = end_date
            for data in self.__worker_schedules[date].get_schedule_generator(
                start_date=start_date,
                end_date=next_date
                if next_date == end_date
                else next_date - timedelta(days=1),
            ):
                yield data
            start_date = next_date

    def get_closest_dates(
        self, start_date: datetime, end_date: datetime
    ) -> list[datetime]:
        """Получить список дат, изменений в расписании.

        :param start_date: Дата начала период.
        :param end_date: Дата окончания период.
        :return: Список дат, изменений в расписании.
        """

        min_date = [list(self.__worker_schedules.keys())[0]]
        for date in self.__worker_schedules.keys():
            if start_date >= date:
                min_date = [date]

        for date in self.__worker_schedules.keys():
            if min_date[-1] != date and min_date[-1] <= date <= end_date:
                min_date.append(date)
        return min_date

    def __str__(self):
        return f"Worker(name={self.name})"

    __repr__ = __str__
