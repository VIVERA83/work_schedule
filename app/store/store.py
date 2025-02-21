from logging import Logger

from store.db.postgres.accessor import PostgresAccessor
from store.work_schedule.car.accessor import CarAccessor
from store.work_schedule.driver.accessor import DriverAccessor
from store.work_schedule.drivers_planner.accessor import DriversPlannerAccessor
from store.work_schedule.schedule_type.accessor import ScheduleTypeAccessor
from store.work_schedule.work_schedule_history.accessor import (
    WorkScheduleHistoryAccessor,
)


class Store:
    def __init__(self, accessor: PostgresAccessor, loger: Logger):
        self.accessor = accessor
        self.driver = DriverAccessor(self.accessor, loger)
        self.car = CarAccessor(self.accessor, loger)
        self.schedule_type = ScheduleTypeAccessor(self.accessor, loger)
        self.work_schedule_history = WorkScheduleHistoryAccessor(self.accessor, loger)
        self.drivers_planner = DriversPlannerAccessor(self.accessor, loger)
        # зависимые от остальных
        # self.drivers_planner_manager = DriversPlannerManager(self.accessor, loger)

    async def connect(self):
        await self.accessor.connect()

    async def disconnect(self):
        await self.accessor.disconnect()
