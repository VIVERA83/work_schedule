from datetime import datetime, timedelta
from typing import Literal

DATE = str
CONVENTIONAL_SIGNS = Literal["Р", "В"]


def timetable_work(
        start: datetime.date = datetime.now(),
        end: datetime.date = datetime.now(),
        is_working: bool = True,
        what_day: int = 1,
        work_days: int = 4,
        weekend_days: int = 2,
        date_format: str = "%d-%m-%Y"

) -> dict[DATE, CONVENTIONAL_SIGNS]:
    """Возвращает расписание работы.

    :param start: Дата начала
    :param end: Дата окончания
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету.  Если is_working = True, какой день счету работает.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param date_format: Формат даты, если не указан, то будет '%d-%m-%Y'
    :return: Словарь, где ключ - дата, значение - 'P' (рабочий день) или 'B' (не рабочий день)

    Для того что бы задать в расписание все рабочие дни необходимо:
    work_days=-1,
    weekend_days=-1,
    is_working=True,
    what_day=1, <----

    Для того что бы задать в расписание все выходные дни необходимо:
    work_days=-1,
    weekend_days=-1,
    is_working=True,
    what_day=0, <----
    """

    result: dict[DATE, CONVENTIONAL_SIGNS] = {}
    total = (end - start).days + 1
    work_day_number = what_day - 1 if is_working else 0
    weekend_day_number = what_day - 1 if not is_working else 0

    for _ in range(total):
        if work_day_number == work_days or weekend_day_number == weekend_days:
            is_working = not is_working
        work_day_number = work_day_number + 1 if is_working else 0
        weekend_day_number = weekend_day_number + 1 if not is_working else 0
        result[start.date().strftime(date_format)] = "Р" if is_working else "В"
        start += timedelta(days=1)
    return result


def is_working_day(schedule_start_date: datetime,
                   work_days: int,
                   weekend_days: int,
                   date: datetime = datetime.now(),
                   is_working: bool = True,
                   what_day: int = 1,
                   ) -> bool:
    """Проверка даты на рабочий день.

    Считывается, что дата рабочего дня равна дате начала расписания.

    :param schedule_start_date: Дата начала расписания.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param date: Дата, которую нужно проверить.
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету. Если is_working = True, какой день счету работает.
    :return: True - рабочий день, False - не рабочий день
    """
    total = (date - schedule_start_date).days + 1
    work_day_number = what_day - 1 if is_working else 0
    weekend_day_number = what_day - 1 if not is_working else 0

    for _ in range(total):
        if work_day_number == work_days or weekend_day_number == weekend_days:
            is_working = not is_working
        work_day_number = work_day_number + 1 if is_working else 0
        weekend_day_number = weekend_day_number + 1 if not is_working else 0
        schedule_start_date += timedelta(days=1)
    return is_working
