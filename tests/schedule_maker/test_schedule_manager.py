from datetime import timedelta, datetime

from icecream import ic

from tests.schedule_maker.data import driver_0_id, driver_0_s, car_id_0, car_0_s, date_06_01_2025, date_10_01_2025, \
    merged_schedule, driver_1_s, driver_1_id, date_17_01_2025, today_1, car_0_name
from work_schedule.store.scheduler.schedule_maker import ScheduleMaker
from work_schedule.store.scheduler.schedule_manager import ScheduleManager


def test_schedule_manager():
    car_schedule = ScheduleMaker(
        car_0_name,
        date_06_01_2025,
        work_days=-1,
        weekend_days=-1,
        is_working=True,
        what_day=1,
    )
    relationship = {
        # car_id_0: [driver_0_id, driver_1_id]
        car_id_0: [driver_0_s, driver_1_s]
    }
    schedule = car_schedule.make_schedule(today_1, today_1 + timedelta(days=10))


    for driver_s in relationship[car_id_0]:
            schedule = driver_s.make_schedule(date_10_01_2025, date_17_01_2025)

            ic(schedule)




    # driver_schedules = {
    #     driver_0_id: driver_0_s,
    #     driver_1_id: driver_1_s
    # }
    # car_schedules = {
    #     car_id_0: car_0_s
    # }

    # manager = ScheduleManager(
    #     driver_schedules=driver_schedules,
    #     car_schedules=car_schedules,
    # )




    # merged = manager.merge_driver_and_car_schedule(driver_0_id, car_id_0, date_06_01_2025, date_10_01_2025)
    # assert merged_schedule == merged
    # ic(driver_0_s.make(date_10_01_2025, date_17_01_2025))
    # date_22_01_2025 = datetime(2025, 1, 22)
    # sh = ic(driver_1_s.make(date_17_01_2025, date_17_01_2025+timedelta(days=10)))
    # time_table = driver_0_s.merge(sh,date_17_01_2025 , date_17_01_2025+timedelta(days=10), driver_1_s.name)
    # ic(time_table)
    # t =car_0_s.merge(time_table,date_17_01_2025 , date_17_01_2025+timedelta(days=10), driver_0_s.name)
    #
    # ic(t)
    # # for car_id, driver_ids in relationship.items():
    #     timetable = car_0_s.make(date_10_01_2025, date_17_01_2025)
    #     for driver_id in driver_ids:
    #         timetable = manager.update_driver_and_car_schedule(driver_id, car_id, date_10_01_2025, date_17_01_2025, timetable)
    #     ic(timetable)

    # ic(merged)
    # ic(driver_1_s.make(date_06_01_2025, date_10_01_2025))


if __name__ == '__main__':
    # TODO  остановился тут
    test_schedule_manager()
