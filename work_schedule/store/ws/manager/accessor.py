from datetime import datetime

from icecream import ic
from store.ws.base.accessor import BaseAccessor
from store.ws.models import DriverModel, WorkScheduleHistoryModel


class ManagerAccessor(BaseAccessor):

    async def create(
            self,
            name: str,
            id_schedule_type: int,
            is_working: bool,
            what_day: int,
            date: datetime,
    ):
        async with self.accessor.session as session:
            driver = DriverModel(name=name)
            session.add(driver)
            await session.flush()
            work_schedule_history = WorkScheduleHistoryModel(
                id_driver=driver.id,
                is_working=is_working,
                id_schedule_type=id_schedule_type,
                what_day=what_day,
                date=date,
            )
            session.add(work_schedule_history)
            await session.commit()
        return driver, work_schedule_history

