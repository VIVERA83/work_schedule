from datetime import datetime

from work_schedule.store.db.data.car import CarDB
from work_schedule.store.db.data.car_driver_assign import CarDriverAssignDB
from work_schedule.store.db.data.dc import Car, CarDriverAssign, DriverFullData
from work_schedule.store.db.data.driver import Driver, DriverDB
from work_schedule.store.db.data.exceptions import DBNotFoundException
from work_schedule.store.db.data.schedule_type import ScheduleType, ScheduleTypeDB
from work_schedule.store.db.data.work_schedule_history import (
    WorkScheduleHistory,
    WorkScheduleHistoryDB,
)
from work_schedule.store.db.utils import validate_schedule_data


class DB:
    def __init__(self):
        self.driver_db = DriverDB()
        self.schedule_type_db = ScheduleTypeDB()
        self.work_schedule_history_db = WorkScheduleHistoryDB()
        self.car_db = CarDB()
        self.car_driver_assign = CarDriverAssignDB()

    def get_driver_by_id(self, id_: int) -> Driver:
        return self.driver_db.get_by_id(id_)

    def get_work_schedule_history_by_id(self, id_: int) -> WorkScheduleHistory:
        return self.work_schedule_history_db.get_by_id(id_)

    def get_schedule_type_by_id(self, id_: int) -> ScheduleType:
        return self.schedule_type_db.get_by_id(id_)

    def get_car_driver_assign_by_id(self, id_: int) -> CarDriverAssign:
        return self.car_driver_assign.get_by_id(id_)

    def get_full_data_driver_by_id(self, id_: int) -> DriverFullData:
        driver = self.get_driver_by_id(id_)
        work_schedule_history = self.get_work_schedule_history_by_id(driver.id)
        schedule_type = self.get_schedule_type_by_id(
            work_schedule_history.id_schedule_type
        )
        try:
            car_driver_assign = self.get_car_driver_assign_by_id(driver.id)
            car = self.car_db.get_by_id(car_driver_assign.id_car)
        except DBNotFoundException:
            car = None

        return DriverFullData(
            driver,
            work_schedule_history,
            schedule_type,
            car,
        )

    def create_driver(
        self,
        name: str,
        schedule_type_id: int,
        is_working: bool = True,
        what_day: int = 1,
    ) -> DriverFullData:
        """Создать запись о водителе.

        Идентификатор создаётся автоматически. Так же добавляется запись о типе расписания.

        :param name: Имя водителя.
        :param schedule_type_id: Идентификатор типа расписания.
        :param is_working: Флаг, работающий ли водитель.
        :param what_day: Который день, водитель работает.
        :return DriverFullData: Полные данные о водителе.
        """
        schedule_type = self.get_schedule_type_by_id(schedule_type_id)
        validate_schedule_data(
            is_working, what_day, schedule_type.work_days, schedule_type.weekend_days
        )

        driver: Driver = self.driver_db.get_combined_employees_work_plans({"name": name})
        work_schedule_history = self.work_schedule_history_db.get_combined_employees_work_plans(
            {
                "id_driver": driver.id,
                "id_schedule_type": schedule_type.id,
                "date": datetime.now(),
                "is_working": is_working,
                "what_day": what_day,
            }
        )
        return DriverFullData(
            driver,
            work_schedule_history,
            schedule_type,
        )

    def get_car_by_id(self, id_: int) -> Car:
        return self.car_db.get_by_id(id_)
