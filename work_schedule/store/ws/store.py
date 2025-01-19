from logging import Logger

from store.db.postgres.accessor import PostgresAccessor
from store.ws.car.accessor import CarAccessor
from store.ws.driver.accessor import DriverAccessor
from store.ws.manager.accessor import ManagerAccessor
from store.ws.schedule_type.accessor import ScheduleTypeAccessor
from store.ws.work_schedule_history.accessor import WorkScheduleHistoryAccessor


class DB:
    def __init__(self, accessor: PostgresAccessor, loger: Logger):
        self.accessor = accessor
        self.driver = DriverAccessor(self.accessor, loger)
        self.car = CarAccessor(self.accessor, loger)
        self.schedule_type = ScheduleTypeAccessor(self.accessor, loger)
        self.work_schedule_history = WorkScheduleHistoryAccessor(self.accessor, loger)
        self.manager = ManagerAccessor(self.accessor, loger)

    async def connect(self):
        await self.accessor.connect()

    async def disconnect(self):
        await self.accessor.disconnect()
