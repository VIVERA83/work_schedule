from work_schedule.store.db.data.dc import DriverFullData
from work_schedule.store.db.data.driver import DriverDB, Driver
from work_schedule.store.db.data.schedule_type import ScheduleTypeDB, ScheduleType
from work_schedule.store.db.data.work_schedule_history import WorkScheduleHistoryDB, WorkScheduleHistory


class DB:
    def __init__(self):
        self.driver_db = DriverDB()
        self.schedule_type_db = ScheduleTypeDB()
        self.work_schedule_history_db = WorkScheduleHistoryDB()

    def get_driver_by_id(self, id_: int) -> Driver:
        return self.driver_db.get_by_id(id_)

    def get_work_schedule_history_by_id(self, id_: int) -> WorkScheduleHistory:
        return self.work_schedule_history_db.get_by_id(id_)

    def get_schedule_type_by_id(self, id_: int) -> ScheduleType:
        return self.schedule_type_db.get_by_id(id_)

    def get_full_data_driver_by_id(self, id_: int) -> DriverFullData:
        driver = self.get_driver_by_id(id_)
        work_schedule_history = self.get_work_schedule_history_by_id(driver.id)
        schedule_type = self.get_schedule_type_by_id(work_schedule_history.id)
        return DriverFullData(
            driver,
            work_schedule_history,
            schedule_type,
        )
