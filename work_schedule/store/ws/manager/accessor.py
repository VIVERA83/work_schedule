from datetime import datetime

from sqlalchemy import RowMapping
from store.ws.base.accessor import BaseAccessor
from store.ws.base.exceptions import exception_handler
from store.ws.manager.exceptions import ForeignKeyException
from store.ws.manager.sql import sql_query_current_worker_schedule
from store.ws.models import (
    CarDriverAssociationModel,
    DriverModel,
    WorkScheduleHistoryModel,
)


class ManagerAccessor(BaseAccessor):
    """Класс для работы с базой данных."""

    @exception_handler(foreign_key=ForeignKeyException)
    async def create(
        self,
        name: str,
        id_schedule_type: int,
        is_working: bool,
        what_day: int,
        date: datetime,
    ):
        """Добавление нового водителя в базу данных и создание новой записи в таблице work_schedule_history.

        Таблица work_schedule_history - назначение, изменения графика работы.

        :param name: Имя водителя
        :param id_schedule_type: Идентификатор типа расписания
        :param is_working: Флаг работы водителя
        :param what_day: Какой день, водитель работает(отдыхает)
        :param date: Дата начала графика
        :return: tuple[DriverModel, WorkScheduleHistoryModel]
        """
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

    @exception_handler()
    async def assign_car_driver(self, driver_id: int, car_id: int):
        """Назначение водителя на автомобиль.

        :param driver_id: Идентификатор водителя
        :param car_id: Идентификатор автомобиля
        :return: CarDriverAssociationModel
        """
        async with self.accessor.session as session:
            assign_car = CarDriverAssociationModel(driver_id=driver_id, car_id=car_id)
            session.add(assign_car)
            await session.commit()
        return assign_car

    @exception_handler()
    async def get_current_worker_schedule_by_id(self, driver_id: int) -> RowMapping:
        smtp = self.accessor.get_query_from_text(sql_query_current_worker_schedule)
        async with self.accessor.session as session:
            result = await session.execute(smtp, {"driver_id": driver_id})
        return result.mappings().one()
