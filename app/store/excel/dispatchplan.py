from collections import defaultdict

from icecream import ic

from driver_scheduling.utils import SIGNAL_WORK, SIGNAL_WEEKEND


class DispatchPlan:
    """Класс для хранения статистических данных."""

    def __init__(self):
        self._table: dict[str, list] = defaultdict(list)
        self._no_driver = defaultdict(int)
        self._repair = defaultdict(int)
        self._total = defaultdict(int)
        self._titles: list[str] = []

    @property
    def no_driver(self) -> dict[str, int]:
        """Количество машин без водителя"""
        return self._no_driver

    @property
    def repair(self) -> dict[str, int]:
        """Количество машин на ремонте"""
        return self._repair

    @property
    def total(self) -> dict[str, int]:
        """Количество машин в наряде"""
        return self._total

    @property
    def table(self) -> dict[str, list]:
        """Таблица с данными"""
        return self._table

    @property
    def titles(self) -> list[str]:
        """Заголовки таблицы"""
        return self._titles


class StatisticCalculator(DispatchPlan):
    """Класс для расчета статистических данных."""

    def __init__(self, work_plan: dict[str, dict[str, str]]):
        super().__init__()
        self.work_plan = work_plan
        self._calculate()

    def _init_static(self):
        """Инициализация данных по дате, назначаем значения по умолчанию"""
        for date in self.work_plan:
            self._no_driver[date] = 0
            self._repair[date] = 0
            self._total[date] = 0

    def _fill_table_data(self):
        """Заполнение таблицы данными"""
        for date, cars in self.work_plan.items():
            for name, value in cars.items():
                self.table[name].append(value)


    def _fill_statistic(self):
        for date, car in self.work_plan.items():
            for name, value in car.items():
                if value == SIGNAL_WORK:
                    self.no_driver[date] += 1
                elif value == SIGNAL_WEEKEND:
                    self.repair[date] += 1
                else:
                    self.total[date] += 1

    def _fill_titles(self):
        self._titles = ["    Машина    ", *[date for date in self.work_plan.keys()]]

    def _calculate(self):
        self._init_static()
        self._fill_table_data()
        self._fill_statistic()
        self._fill_titles()
