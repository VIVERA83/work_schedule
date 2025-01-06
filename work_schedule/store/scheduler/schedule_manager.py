from datetime import datetime

from work_schedule.store.scheduler.schedule_maker import ScheduleMaker


class ScheduleManager:

    def __init__(self,
                 driver_schedules: dict[int, ScheduleMaker],
                 car_schedules: dict[int, ScheduleMaker],
                 ) -> None:
        self.driver_schedules = driver_schedules
        self.car_schedules = car_schedules

    def _get_schedule(self,
                      id_: int,
                      is_driver: bool) -> ScheduleMaker:
        if schedule := self.driver_schedules.get(id_, None) if is_driver else self.car_schedules.get(id_, None):
            return schedule
        error_msg = f"Не найдено расписание для {'Водителя' if is_driver else 'Автомобиля'} с id = {id_}"
        raise ValueError(error_msg)

    def get_driver_schedule(self, id_: int, ) -> ScheduleMaker:
        return self._get_schedule(id_, is_driver=True)

    def get_car_schedule(self, id_: int, ) -> ScheduleMaker:
        return self._get_schedule(id_, is_driver=False)

    def get_merge_driver_and_car_schedule(self,
                                          driver_id: int,
                                          car_id: int,
                                          start_date: datetime,
                                          end_date: datetime) -> list[str]:
        car_schedule = self.get_car_schedule(car_id)
        driver_schedule = self.get_driver_schedule(driver_id)
        result = []
        for car, driver in zip(car_schedule.make(start_date, end_date).items(),
                               driver_schedule.make(start_date, end_date).items()):
            if car == driver:
                result.append(driver_schedule.name)
            else:
                result.append(car[1])
        return result
