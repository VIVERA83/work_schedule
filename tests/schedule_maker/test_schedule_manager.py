from icecream import ic

from tests.schedule_maker.data import driver_0_id, driver_0_s, car_id_0, car_0_s, date_06_01_2025, date_10_01_2025, \
    merged_schedule, driver_1_s, driver_1_id
from work_schedule.store.scheduler.schedule_manager import ScheduleManager


def test_schedule_manager():
    driver_schedules = {
        driver_0_id: driver_0_s,
        driver_1_id: driver_1_s
    }
    car_schedules = {
        car_id_0: car_0_s
    }
    relationship = {
        car_id_0: [driver_0_id, driver_0_id]
    }
    manager = ScheduleManager(
        driver_schedules=driver_schedules,
        car_schedules=car_schedules,
    )
    merged = manager.get_merge_driver_and_car_schedule(driver_0_id, car_id_0, date_06_01_2025, date_10_01_2025)
    assert merged_schedule == merged
    ic(merged)
    ic(driver_1_s.make(date_06_01_2025, date_10_01_2025))


if __name__ == '__main__':
    test_schedule_manager()
