from datetime import datetime, timedelta

from icecream import ic

from tests.schedule_maker.data import (
    car_0_name,
    car_0_s,
    car_id_0,
    date_06_01_2025,
    date_10_01_2025,
    date_17_01_2025,
    driver_0_id,
    driver_0_s,
    driver_1_id,
    driver_1_s,
    merged_schedule,
    today_1,
)
from work_schedule.store.scheduler.worker_schedule import WorkerSchedule


class ScheduleManager:

    def __init__(
        self,
        driver_schedules: dict[int, WorkerSchedule],
        car_schedules: dict[int, WorkerSchedule],
    ) -> None:
        self.driver_schedules = driver_schedules
        self.car_schedules = car_schedules

    def _get_schedule(self, id_: int, is_driver: bool) -> WorkerSchedule:
        if schedule := (
            self.driver_schedules.get(id_, None)
            if is_driver
            else self.car_schedules.get(id_, None)
        ):
            return schedule
        error_msg = f"Не найдено расписание для {'Водителя' if is_driver else 'Автомобиля'} с id = {id_}"
        raise ValueError(error_msg)

    def get_driver_schedule(
        self,
        id_: int,
    ) -> WorkerSchedule:
        return self._get_schedule(id_, is_driver=True)

    def get_car_schedule(
        self,
        id_: int,
    ) -> WorkerSchedule:
        return self._get_schedule(id_, is_driver=False)

    def merge_driver_and_car_schedule(
        self,
        driver_id: int,
        car_id: int,
        start_date: datetime,
        end_date: datetime,
    ) -> list[str]:
        car_schedule = self.get_car_schedule(car_id)
        driver_schedule = self.get_driver_schedule(driver_id)
        timetable = []
        for car, driver in zip(
            car_schedule.get_schedule(start_date, end_date).items(),
            driver_schedule.get_schedule(start_date, end_date).items(),
        ):
            if car == driver:
                timetable.append(driver_schedule.name)
            else:
                timetable.append(car[1])
        return timetable

    def update_driver_and_car_schedule(
        self,
        driver_id: int,
        car_id: int,
        start_date: datetime,
        end_date: datetime,
        timetable: dict[str, str],
    ) -> dict[str, str]:
        car_schedule = self.get_car_schedule(car_id)
        driver_schedule = self.get_driver_schedule(driver_id)
        for car, driver, day in zip(
            car_schedule.get_schedule(start_date, end_date).items(),
            driver_schedule.get_schedule(start_date, end_date).items(),
            timetable.copy().items(),
        ):
            if car == driver == day:
                timetable[day[0]] = driver_schedule.name
        return timetable


def test_schedule_manager():
    car_schedule = WorkerSchedule(
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
    schedule = car_schedule.get_schedule(today_1, today_1 + timedelta(days=10))

    for driver_s in relationship[car_id_0]:
        schedule = driver_s.get_schedule(date_10_01_2025, date_17_01_2025)

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


if __name__ == "__main__":
    # TODO  остановился тут
    test_schedule_manager()
