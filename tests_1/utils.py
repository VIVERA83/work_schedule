from logging import Logger

from store.db.postgres.accessor import PostgresAccessor
from store.ws.car.accessor import CarAccessor
from store.ws.driver.accessor import DriverAccessor
from store.ws.manager.accessor import ManagerAccessor


def validate_schedule_data(
    is_working: bool, what_day: int, work_days: int, weekend_days: int
) -> None:
    if is_working and not (work_days >= what_day > 0):
        raise ValueError(
            f"Неверное значение параметра {what_day=} в диапазоне от 1 до {work_days=}."
        )
    elif not (weekend_days >= what_day > 0):
        raise ValueError(
            f"Неверное значение параметра {what_day=} в диапазоне от 1 до {weekend_days=}."
        )


class DB:
    def __init__(self, accessor: PostgresAccessor, loger: Logger):
        self.accessor = accessor
        self.driver = DriverAccessor(self.accessor, loger)
        self.car = CarAccessor(self.accessor, loger)
        self.manager = ManagerAccessor(self.accessor, loger)

    async def connect(self):
        await self.accessor.connect()

    async def disconnect(self):
        await self.accessor.disconnect()
