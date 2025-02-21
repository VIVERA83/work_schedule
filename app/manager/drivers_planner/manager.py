from datetime import datetime

from typing import Any

from api.worker_schedule.schemes import CrewSchema
from driver_scheduling.crew_manager import CrewsManager

from driver_scheduling.schedule_manager import ScheduleManager
from driver_scheduling.worker_schedule import WorkerSchedule
from excel.excel import Excel
from manager.base.exceptions import exception_handler
from manager.drivers_planner.utils import create_file_name
from store.excel.crew_sheet import CrewSheet
from store.excel.dispatchplan import StatisticCalculator, DispatchPlan
from manager.base.manager import BaseManager


class DriversPlannerManager(BaseManager):
    @exception_handler("get_schedule")
    async def get_schedule(
        self, id_: int, start_date: datetime, end_date: datetime
    ) -> dict[str, Any]:
        """Возвращает график работы водителя по id.
        :param id_: Идентификатор водителя
        :param start_date: Начало диапазона
        :param end_date: Конец диапазона
        :return: dict[str, Any]
        """
        result = await self.store.drivers_planner.get_current_worker_schedule_by_id(id_)
        return WorkerSchedule(**result).get_schedule(start_date, end_date)

    @exception_handler("export_driver_schedule_to_excel")
    async def export_driver_schedule_to_excel(
        self, start_date: datetime, end_date: datetime
    ) -> str:
        """Экспорт графика работы водителя в Excel.
        :param start_date: Начало диапазона
        :param end_date: Конец диапазона
        :return: имя файла сохраненного в Excel
        """
        self.logger.info("Начало экспорта графика в Excel")
        row_crews = await self.store.drivers_planner.get_crew_schedule(
            start_date, end_date
        )
        self.logger.debug("Данные экипажей получены")
        data = self.__convert_data_to_schedule_drivers(row_crews)
        self.logger.debug("Данные экипажей преобразованы")
        static = self.get_statistic(start_date, end_date, data)
        self.logger.debug("Статистика рассчитана")
        file_name = create_file_name(start_date, end_date)
        self.logger.info(f"Файл будет сохранен как {file_name}")
        self.__export_to_excel(file_name, static)
        self.logger.info("Экспорт завершен")
        return file_name

    @staticmethod
    def __convert_data_to_schedule_drivers(row_crews) -> dict[str, CrewSchema]:
        """Преобразование данных в график работы водителя."""
        return {
            item[0]: CrewSchema(id=item[0], cars=item[1], drivers=item[2])
            for item in row_crews
        }

    @staticmethod
    def get_statistic(
        start_date: datetime, end_date: datetime, dict_crews
    ) -> StatisticCalculator:
        """Получение статистики по графику работы водителей.

        :param start_date: Начало диапазона
        :param end_date: Конец диапазона
        :param dict_crews: Данные экипажей
        :return: StatisticCalculator
        """
        combined_employees_work_plans = CrewsManager(dict_crews, start_date, end_date)()
        manager = ScheduleManager()
        for combined_employees_work_plan in combined_employees_work_plans.values():
            manager.add_combined_employees_work_plan(combined_employees_work_plan)

        data = manager.get_schedule(start_date, end_date)
        return StatisticCalculator(data)

    @staticmethod
    def __export_to_excel(file_name, dispatch_plan: DispatchPlan):
        """Экспорт данных в Excel.

        :param file_name: Имя файла
        :param dispatch_plan: Данные для экспорта
        """
        excel = Excel()
        sheet = excel.create_sheet("График работы")
        CrewSheet(dispatch_plan, sheet).fill_in_data_sheet()
        excel.save(file_name)
