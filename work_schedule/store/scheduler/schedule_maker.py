from datetime import datetime
from functools import wraps
from typing import Generator, Callable, ParamSpec, TypeVar

from work_schedule.store.scheduler.utils import get_timetable_period, \
    generator_timetable_period, validate_make_date, DATE_FORMAT, DATE, SIGN

_PWrapped = ParamSpec('_PWrapped')
_RWrapped = TypeVar('_RWrapped')


class WorkerSchedule:
    """График работы."""

    def __init__(self,
                 name: str,
                 schedule_start_date: datetime,
                 work_days: int,
                 weekend_days: int,
                 is_working: bool,
                 what_day: int,
                 date_format: str = DATE_FORMAT
                 ):
        self.name = name
        self.schedule_start_date = schedule_start_date
        self.work_days = work_days
        self.weekend_days = weekend_days
        self.is_working = is_working
        self.what_day = what_day
        self.date_format = date_format

    def __check_make_data(self: Callable[_PWrapped, _RWrapped]) -> Callable[_PWrapped, _RWrapped]:
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
            validate_make_date(cls.schedule_start_date, start_date, end_date)
            return self(cls, start_date, end_date, *args, **kwargs)

        return wrapper

    @__check_make_data  # noqa
    def make_schedule(self, start_date: datetime, end_date: datetime) -> dict[DATE, SIGN]:
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
    def make_schedule_generator(self, start_date: datetime, end_date: datetime) -> Generator[
        tuple[DATE, SIGN], DATE, None]:
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
            if buffer is not None and datetime.strptime(buffer, self.date_format) > datetime.strptime(date,
                                                                                                      self.date_format):
                continue
            next_date = (yield date, signal)
