from store.ws.base.accessor import BaseAccessor
from store.ws.models import DriverModel, WorkScheduleHistoryModel


class ManagerAccessor(BaseAccessor):

    async def create(self, name: str, id_schedule_type: int, is_working: bool, what_day: int) -> tuple[
        DriverModel, WorkScheduleHistoryModel]:
        driver = DriverModel(name=name)
        work_schedule_history = WorkScheduleHistoryModel(
            driver=driver,
            is_working=is_working,
            id_schedule_type=id_schedule_type,
            what_day=what_day)
        async with self.accessor.session as session:
            session.add_all([driver,work_schedule_history])
            await session.commit()
        return driver, work_schedule_history


    