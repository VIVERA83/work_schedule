from datetime import datetime

from sqlalchemy import RowMapping
from store.ws.base.accessor import BaseAccessor
from store.ws.base.exceptions import exception_handler
from store.ws.manager.exceptions import ForeignKeyException
from store.ws.manager.sql import sql_query_current_worker_schedule, get_sql_query_crews
from store.ws.models import (

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

    async def get_all_crews(self, start_date: datetime, end_date: datetime) -> list:
        """Получить список экипажей с графиками работы в указанный диапазон времени.

        :param start_date: Начало диапазона
        :param end_date: Конец диапазона
        :return: list
        """
        sql = get_sql_query_crews(self.accessor.settings.postgres_schema, start_date, end_date)
        async with self.accessor.session as session:
            result = await session.execute(sql)
            return list(result.all())

    # async def all(self, start_date: datetime, end_date: datetime):
    #     async with self.accessor.session as session:
    #         result = self.accessor.get_query_select_by_model(CarModel)
    #         data = await session.execute(result)
    #
