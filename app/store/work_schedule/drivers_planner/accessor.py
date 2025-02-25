from datetime import datetime

from sqlalchemy import RowMapping
from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.base.exceptions import exception_handler
from store.work_schedule.drivers_planner.exceptions import (
    DriverScheduleNotFoundException,
)

from store.work_schedule.drivers_planner.sql import (
    get_sql_query_current_worker_schedule,
    get_sql_query_crews,
)


class DriversPlannerAccessor(BaseAccessor):
    @exception_handler(not_found=DriverScheduleNotFoundException)
    async def get_current_worker_schedule_by_id(self, driver_id: int) -> RowMapping:
        """Получение текущего графика работы водителя.

        Выводит последний график работы водителя.

        :param driver_id: Идентификатор водителя
        :return: RowMapping
        """
        sql = get_sql_query_current_worker_schedule(self.accessor.settings.postgres_schema)
        async with self.accessor.session as session:
            result = await session.execute(sql, {"driver_id": driver_id})
        return result.mappings().one()

    async def get_crew_schedule(self, start_date: datetime, end_date: datetime) -> list:
        """Получить список экипажей с графиками работы в указанный диапазон времени.

        :param start_date: Начало диапазона
        :param end_date: Конец диапазона
        :return: list
        """
        sql = get_sql_query_crews(
            self.accessor.settings.postgres_schema, start_date, end_date
        )
        async with self.accessor.session as session:
            result = await session.execute(sql)
            return list(result.all())
