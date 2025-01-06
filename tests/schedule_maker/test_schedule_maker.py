from tests.schedule_maker.data import (
    name,
    date_17_01_2020,
    work_days_4,
    weekend_days_2,
    is_working_true,
    what_day_1, date_01_01_2020, date_17_02_2020,
)
from work_schedule.store.schedule_maker.schedule_maker import ScheduleMaker

schedule = ScheduleMaker(
    name=name,
    schedule_start_date=date_17_01_2020,
    work_days=work_days_4,
    weekend_days=weekend_days_2,
    is_working=is_working_true,
    what_day=what_day_1
)


def test_schedule_maker__validate_make_data():
    try:
        schedule.validate_make_data(date_17_02_2020, date_17_01_2020)
        assert False, ("Должна быть ошибка при попытке создать расписание. "
                       "Значение start_date должно быть меньше end_date.")
    except ValueError:
        ...
    try:
        schedule.validate_make_data(date_01_01_2020, date_17_02_2020)
        assert False, ("Должна быть ошибка при попытке создать расписание. "
                       "Значение start_date должно быть больше schedule_start_date.")
    except ValueError:
        ...
    try:
        schedule.validate_make_data(date_01_01_2020, date_01_01_2020)
        assert False, ("Должна быть ошибка при попытке создать расписание. "
                       "Значение start_date должно быть больше schedule_start_date.")
    except ValueError:
        ...
    schedule.validate_make_data(date_17_01_2020, date_17_02_2020)
    print("test_schedule_maker__validate_make_data OK")


if __name__ == "__main__":
    test_schedule_maker__validate_make_data()
