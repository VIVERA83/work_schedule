from datetime import datetime, timedelta
from typing import Generator, Literal

DATE_FORMAT = "%d-%m-%Y"
DATE = str
SIGNAL_WEEKEND: str = "B"
SIGNAL_WORK: str = "P"
SIGN = Literal[SIGNAL_WEEKEND, SIGNAL_WORK]  # noqa


def timetable_work(
    start: datetime = datetime.now(),
    end: datetime = datetime.now(),
    is_working: bool = True,
    what_day: int = 1,
    work_days: int = 4,
    weekend_days: int = 2,
    date_format: str = DATE_FORMAT,
) -> dict[DATE, SIGN]:
    """Возвращает расписание работы.

    :param start: Дата начала
    :param end: Дата окончания
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету.  Если is_working = True, какой день счету работает.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param date_format: Формат даты, если не указан, то будет DATE_FORMAT (смотри значение выше)
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

    result: dict[DATE, SIGN] = {}
    total = date_subtraction(end, start) + 1

    work_day_number = what_day - 1 if is_working else 0
    weekend_day_number = what_day - 1 if not is_working else 0

    for _ in range(total):
        if work_day_number == work_days or weekend_day_number == weekend_days:
            is_working = not is_working
        work_day_number = work_day_number + 1 if is_working else 0
        weekend_day_number = weekend_day_number + 1 if not is_working else 0
        result[start.date().strftime(date_format)] = (
            SIGNAL_WORK if is_working else SIGNAL_WEEKEND
        )
        start += timedelta(days=1)
    return result


def is_working_day(
    schedule_start_date: datetime,
    work_days: int,
    weekend_days: int,
    date: datetime = datetime.now(),
    is_working: bool = True,
    what_day: int = 1,
) -> tuple[bool, int]:
    """Проверка даты на рабочий день, и какой день счету работает(отдыхает).

    Считывается, что дата рабочего дня равна дате начала расписания.

    :param schedule_start_date: Дата начала расписания.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param date: Дата, которую нужно проверить.
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету. Если is_working = True, какой день счету работает.
    :return: True - рабочий день, False - не рабочий день и какой день счету работает(отдыхает).
    """
    total = date_subtraction(date, schedule_start_date) + 1
    work_day_number = what_day - 1 if is_working else 0
    weekend_day_number = what_day - 1 if not is_working else 0

    for _ in range(total):
        if work_day_number == work_days or weekend_day_number == weekend_days:
            is_working = not is_working
        work_day_number = work_day_number + 1 if is_working else 0
        weekend_day_number = weekend_day_number + 1 if not is_working else 0
        schedule_start_date += timedelta(days=1)
    return is_working, work_day_number if is_working else weekend_day_number


def get_timetable_period(
    schedule_start_date: datetime,
    work_days: int,
    weekend_days: int,
    is_working: bool,
    what_day: int,
    start_date: datetime,
    end_date: datetime,
    date_format: str = DATE_FORMAT,
):
    """Получить расписание работы за период.

    Расчет производится на основании даты начала расписания. Для расчета используется параметры
     schedule_start_date, work_days, weekend_days, is_working, what_day: это данные с начала расписания.

    :param schedule_start_date: Дата начала расписания.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету. Если is_working = True, какой день счету работает.
    :param start_date: Дата начала периода.
    :param end_date: Дата окончания периода.
    :param date_format: Формат даты, если не указан, то будет DATE_FORMAT (смотри значение выше)
    :return: Словарь, где ключ - дата, значение - SIGNAL_WORK (рабочий день) или SIGNAL_WEEKEND (не рабочий день).
    """
    # находим заданию дату работает или нет и какой день
    is_work, day = is_working_day(
        schedule_start_date=schedule_start_date,
        work_days=work_days,
        weekend_days=weekend_days,
        date=start_date,
        is_working=is_working,
        what_day=what_day,
    )
    return timetable_work(
        start=start_date,
        end=end_date,
        is_working=is_work,
        what_day=day,
        work_days=work_days,
        weekend_days=weekend_days,
        date_format=date_format,
    )


def date_subtraction(date_1: datetime, date_2: datetime) -> int:
    """Вычитает две даты, при расчетах отбрасываются часы.

    :param date_1: Дата из которой вычитаем.
    :param date_2: Дата, которую вычитаем
    :return int: Разность дней.
    """
    return (
        datetime(year=date_1.year, month=date_1.month, day=date_1.day)
        - datetime(year=date_2.year, month=date_2.month, day=date_2.day)
    ).days


def generator_timetable_work(
    start: datetime = datetime.now(),
    end: datetime = datetime.now(),
    is_working: bool = True,
    what_day: int = 1,
    work_days: int = 4,
    weekend_days: int = 2,
    date_format: str = DATE_FORMAT,
) -> Generator[tuple[DATE, SIGN], None, None]:
    """Генератор расписание работы.

    :param start: Дата начала
    :param end: Дата окончания
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету.  Если is_working = True, какой день счету работает.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param date_format: Формат даты, если не указан, то будет DATE_FORMAT (смотри значение выше)
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

    total = date_subtraction(end, start) + 1

    work_day_number = what_day - 1 if is_working else 0
    weekend_day_number = what_day - 1 if not is_working else 0

    for _ in range(total):
        if work_day_number == work_days or weekend_day_number == weekend_days:
            is_working = not is_working
        work_day_number = work_day_number + 1 if is_working else 0
        weekend_day_number = weekend_day_number + 1 if not is_working else 0
        yield (
            start.date().strftime(date_format),
            (SIGNAL_WORK if is_working else SIGNAL_WEEKEND),
        )
        start += timedelta(days=1)


def generator_timetable_period(
    schedule_start_date: datetime,
    work_days: int,
    weekend_days: int,
    is_working: bool,
    what_day: int,
    start_date: datetime,
    end_date: datetime,
    date_format: str = DATE_FORMAT,
) -> Generator[tuple[DATE, SIGN], None, None]:
    """Генератор расписание работы за период.

    Расчет производится на основании даты начала расписания. Для расчета используется параметры
     schedule_start_date, work_days, weekend_days, is_working, what_day: это данные с начала расписания.

    :param schedule_start_date: Дата начала расписания.
    :param work_days: Количество рабочих дней в смене.
    :param weekend_days: Количество выходных дней в смене.
    :param is_working: Рабочий день = True, Не рабочий день = False
    :param what_day: Какой день по счету. Если is_working = True, какой день счету работает.
    :param start_date: Дата начала периода.
    :param end_date: Дата окончания периода.
    :param date_format: Формат даты, если не указан, то будет DATE_FORMAT (смотри значение выше)
    :return: Кортеж, 1й элемент - дата, 2й - элемент - SIGNAL_WORK (рабочий день) или SIGNAL_WEEKEND (не рабочий день).
    """
    # находим заданию дату работает или нет и какой день
    is_work, day = is_working_day(
        schedule_start_date=schedule_start_date,
        work_days=work_days,
        weekend_days=weekend_days,
        date=start_date,
        is_working=is_working,
        what_day=what_day,
    )
    return generator_timetable_work(
        start=start_date,
        end=end_date,
        is_working=is_work,
        what_day=day,
        work_days=work_days,
        weekend_days=weekend_days,
        date_format=date_format,
    )


def validate_make_date(
    schedule_start_date: datetime, start_date: datetime, end_date: datetime
):
    """Проверка корректности введенных дат.

    Дата начало периода должна быть в границах даты начала расписания и даты окончания периода
    Дата окончания периода должна быть в границах даты начала расписания и даты окончания периода.
    При не соответствии корректности введенных дат генерируется исключение ValueError.

    :param schedule_start_date: Дата начала расписания.
    :param start_date: Дата начала период.
    :param end_date: Дата окончания период.

    """
    start_date = datetime(
        year=start_date.year, month=start_date.month, day=start_date.day
    )
    end_date = datetime(year=end_date.year, month=end_date.month, day=end_date.day)
    err_msg = "\n"
    index = 0
    if start_date < schedule_start_date:
        index += 1
        err_msg += f"{index}. Значение start_date должно быть больше или равно schedule_start_date.\n"
    if end_date < schedule_start_date:
        index += 1
        err_msg += f"{index}. Значение end_date должно быть больше или равно schedule_start_date\n"
    if start_date > end_date:
        index += 1
        err_msg += (
            f"{index}. Значение start_date должно быть меньше или равно end_date.\n"
        )
    if err_msg != "\n":
        raise ValueError(err_msg)
