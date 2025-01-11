from datetime import datetime

from work_schedule.store.scheduler.schedule_maker import WorkerSchedule


class ScheduleManager:

    def __init__(self,
                 driver_schedules: dict[int, WorkerSchedule],
                 car_schedules: dict[int, WorkerSchedule],
                 ) -> None:
        self.driver_schedules = driver_schedules
        self.car_schedules = car_schedules

    def _get_schedule(self,
                      id_: int,
                      is_driver: bool) -> WorkerSchedule:
        if schedule := self.driver_schedules.get(id_, None) if is_driver else self.car_schedules.get(id_, None):
            return schedule
        error_msg = f"Не найдено расписание для {'Водителя' if is_driver else 'Автомобиля'} с id = {id_}"
        raise ValueError(error_msg)

    def get_driver_schedule(self, id_: int, ) -> WorkerSchedule:
        return self._get_schedule(id_, is_driver=True)

    def get_car_schedule(self, id_: int, ) -> WorkerSchedule:
        return self._get_schedule(id_, is_driver=False)

    def merge_driver_and_car_schedule(self,
                                      driver_id: int,
                                      car_id: int,
                                      start_date: datetime,
                                      end_date: datetime,
                                      ) -> list[str]:
        car_schedule = self.get_car_schedule(car_id)
        driver_schedule = self.get_driver_schedule(driver_id)
        timetable = []
        for car, driver in zip(car_schedule.make_schedule(start_date, end_date).items(),
                               driver_schedule.make_schedule(start_date, end_date).items()):
            if car == driver:
                timetable.append(driver_schedule.name)
            else:
                timetable.append(car[1])
        return timetable

    def update_driver_and_car_schedule(self,
                                       driver_id: int,
                                       car_id: int,
                                       start_date: datetime,
                                       end_date: datetime,
                                       timetable: dict[str, str],
                                       ) -> dict[str, str]:
        car_schedule = self.get_car_schedule(car_id)
        driver_schedule = self.get_driver_schedule(driver_id)
        for car, driver, day in zip(car_schedule.make_schedule(start_date, end_date).items(),
                               driver_schedule.make_schedule(start_date, end_date).items(),
                               timetable.copy().items()):
            if car == driver == day:
                timetable[day[0]] = driver_schedule.name
        return timetable
