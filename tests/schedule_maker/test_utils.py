from tests.schedule_maker.data import date_17_01_2020, date_01_01_2020, date_17_01_2021, date_17_02_2020
from work_schedule.store.schedule_maker.utils import dates_comparison


def test_dates_comparison():
    assert dates_comparison(date_17_01_2020,
                            date_17_01_2020) == True, "Если даты равны, то возвращается True"
    assert dates_comparison(date_01_01_2020,
                            date_17_01_2020) == False, "Если первая дата меньше второй, то возвращается False"
    assert dates_comparison(date_17_01_2021,
                            date_17_02_2020) == True, "Если первая дата больше второй, то возвращается True"
    print("test_dates_comparison OK")


if __name__ == "__main__":
    test_dates_comparison()
