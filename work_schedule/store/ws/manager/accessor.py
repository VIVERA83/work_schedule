from icecream import ic
from store.ws.base.accessor import BaseAccessor
from store.ws.models import DriverModel, WorkScheduleHistoryModel


class ManagerAccessor(BaseAccessor):
    class Meta:
        model = None

    # async def create(
    #     self, name: str, id_schedule_type: int, is_working: bool, what_day: int
    # ) -> tuple[DriverModel, WorkScheduleHistoryModel]:
    #     driver = DriverModel(name=name)
    #     work_schedule_history = WorkScheduleHistoryModel(
    #         # driver=driver,
    #         is_working=is_working,
    #         id_schedule_type=id_schedule_type,
    #         what_day=what_day,
    #     )
    #     async with self.accessor.session as session:
    #         session.add_all([driver, work_schedule_history])
    #         await session.commit()
    #     return driver, work_schedule_history

    # async def create(
    #     self, name: str, id_schedule_type: int, is_working: bool, what_day: int
    # ):
    #     async with self.accessor.session as session:
    #         smtp = self.accessor.get_query_from_text(
    #             """WITH par_key AS
    #                (INSERT INTO work_schedule.driver (name)
    #                 VALUES (:name) RETURNING id)
    #                 INSERT INTO work_schedule.work_schedule_history (id_driver, id_schedule_type, is_working, what_day)
    #                 SELECT par_key.id, :id_schedule_type, :is_working, :what_day
    #                 FROM par_key;
    #             """
    #         )
    #     result = await session.execute(
    #         smtp,
    #         {
    #             "name": name,
    #             "id_schedule_type": id_schedule_type,
    #             "is_working": is_working,
    #             "what_day": what_day,
    #         },
    #     )
    #     return result

    async def create(
        self,
        name: str,
        id_schedule_type: int,
        is_working: bool,
        what_day: int,
        id_driver: int,
        date=None,
    ):
        ic(id_driver)
        async with self.accessor.session as session:
            driver = DriverModel(name=name)
            session.add(driver)
            await session.flush()
            work_schedule_history = WorkScheduleHistoryModel(
                id_driver=driver.id,
                is_working=is_working,
                id_schedule_type=id_schedule_type,
                what_day=what_day,
            )
            session.add(work_schedule_history)
            await session.commit()
        return driver, work_schedule_history
