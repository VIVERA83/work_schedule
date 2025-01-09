from tests.schedule_maker.data import (
    date_17_01_2020,
    date_01_01_2020, date_17_02_2020,
    date_06_01_2025, date_10_01_2025,
    car_0_schedule_make_result, driver_0_schedule_make_result, merged_schedule,
    schedule, car_0_s, driver_0_s, today_2, today_1,
)


def test_schedule_maker__validate_make_data():
    try:
        schedule.validate_make_data(date_17_02_2020, date_17_01_2020)
        assert False, ("Должна быть ошибка при попытке создать расписание. "
                       "Значение start_date должно быть меньше или равно end_date.")
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
    schedule.validate_make_data(today_1, today_2)
    print("test_schedule_maker__validate_make_data OK")


def test_schedule_maker__make():
    # проверка, что можно задать все рабочие дни
    assert car_0_schedule_make_result == car_0_s.make_schedule(date_06_01_2025, date_10_01_2025)
    # проверка, проверка на корректность составления расписания
    assert driver_0_schedule_make_result == driver_0_s.make_schedule(date_06_01_2025, date_10_01_2025)
    print("test_schedule_maker__make OK")


def test_schedule_maker_1():
    """Наложение расписаний Водителя и машины."""
    result = []
    for car, driver in zip(car_0_s.make_schedule(date_06_01_2025, date_10_01_2025).items(),
                           driver_0_s.make_schedule(date_06_01_2025, date_10_01_2025).items()):
        if car == driver:
            result.append(driver_0_s.name)
        else:
            result.append(car[1])
    assert merged_schedule == result, "Графики не совпадают."
    print("test_schedule_maker_1 OK")


if __name__ == "__main__":
    test_schedule_maker__validate_make_data()
    test_schedule_maker__make()
    test_schedule_maker_1()
