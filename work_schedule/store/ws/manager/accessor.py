from datetime import datetime

from icecream import ic
from sqlalchemy import RowMapping, text
from store.ws.base.accessor import BaseAccessor
from store.ws.base.exceptions import exception_handler
from store.ws.manager.exceptions import ForeignKeyException, InternalDatabaseException
from store.ws.manager.sql import sql_query_current_worker_schedule
from store.ws.models import (
    # CarDriverAssociationModel,
    DriverModel,
    WorkScheduleHistoryModel,
    CarModel,
    CarScheduleHistoryModel,
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
        self.accessor.logger.debug(f"{self.__class__.__name__}.create : "
                                   f"{name=}, {id_schedule_type=}, {is_working=}, {what_day=}, {date=}")
        async with self.accessor.session as session:
            driver = DriverModel(name=name)
            session.add(driver)
            await session.flush()
            self.accessor.logger.debug(f"{self.__class__.__name__}.create : {driver} успешно создан")
            work_schedule_history = WorkScheduleHistoryModel(
                id_driver=driver.id,
                is_working=is_working,
                id_schedule_type=id_schedule_type,
                what_day=what_day,
                date=date,
            )
            self.accessor.logger.debug(f"{self.__class__.__name__}.create : {work_schedule_history} успешно создан")
            self.accessor.logger.debug(f"{self.__class__.__name__}.create : {work_schedule_history.as_dict}")
            session.add(work_schedule_history)
            await session.commit()
            self.accessor.logger.debug(f"{self.__class__.__name__}.create : {driver} {work_schedule_history} успешно")
        return driver, work_schedule_history

    @exception_handler()
    async def get_current_worker_schedule_by_id(self, driver_id: int) -> RowMapping:
        """Получение текущего графика работы водителя.

        Выводит последний график работы водителя.

        :param driver_id: Идентификатор водителя
        :return: RowMapping
        """
        smtp = self.accessor.get_query_from_text(sql_query_current_worker_schedule)
        async with self.accessor.session as session:
            result = await session.execute(smtp, {"driver_id": driver_id})
        return result.mappings().one()

    @exception_handler()
    async def add_car_set_schedule(
        self,
        name: str,
        car_model: str,
        car_number: str,
        id_schedule_type: int,
        is_working: bool,
        what_day: int,
        date: datetime,
    ):
        """Добавить новую машину в базу данных и назначить график работы(ППО) для машины.

        :param name: Производитель, завод изготовитель
        :param car_model: Модель машины
        :param car_number: Номер машины
        :param id_schedule_type: Идентификатор типа расписания
        :param is_working: Флаг работы машины (то есть рабочий = True, не рабочий = False)
        :param what_day: Какой день, машина работает(отдыхает)
        :param date: Дата начала графика
        :return: tuple[CarModel, CarScheduleHistoryModel]
        """
        async with self.accessor.session as session:
            car = CarModel(name=name, car_model=car_model, car_number=car_number)
            session.add(car)
            await session.flush()
            self.logger.debug(f"{self.__class__.__name__}.add_car_set_schedule : {car} успешно создан")
            car_schedule_history = CarScheduleHistoryModel(
                id_car=car.id,
                is_working=is_working,
                id_schedule_type=id_schedule_type,
                what_day=what_day,
                date=date,
            )
            session.add(car_schedule_history)
            await session.commit()
            self.logger.debug(f"{self.__class__.__name__}.add_car_set_schedule : {car} {car_schedule_history} успешно")
        return car, car_schedule_history

    async def all(self, start_date: datetime, end_date: datetime):
        async with self.accessor.session as session:
            result = self.accessor.get_query_select_by_model(CarModel)
            data = await session.execute(result)
            ic(data.all())
        ...

    async def get_all_bak(self, car_id: int, start_date: datetime, end_date: datetime):
        """Получение всех данных для построения графика работы водителя.

        Запрос возвращает водителей с данными для построения графика работы на машине.
        """
        sql = text(
            f"""
        select
            d."name",
            work_schedule.all_ok('{start_date}', '{end_date}', cda.driver_id)
            from work_schedule.car_driver_association cda
            join work_schedule.driver d on d.id = cda.driver_id
            join work_schedule.car c on c.id  = cda.car_id 
            join work_schedule.work_schedule_history wsh on wsh.id_driver = cda.driver_id  
        where cda.car_id = '{car_id}'::integer
        group by 
            cda.driver_id,
            d.name
        order by 
            cda.driver_id
        ;
        """
        )
        async with self.accessor.session as session:
            result = await session.execute(sql)
            return result.all()
