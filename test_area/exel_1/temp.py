from typing import Literal
from collections import defaultdict
import openpyxl
from openpyxl.styles import PatternFill, Alignment, Border, Side

from store.excel.excel import Excel
from test_area.exel_1.excel import CrewExel
from test_area.exel_1.statistic import StatisticCalculator

# SIGNAL_WEEKEND: str = "B"
# SIGNAL_WORK: str = "P"
# SIGN = Literal[SIGNAL_WEEKEND, SIGNAL_WORK]  # noqa
# black_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
# orange_fill = PatternFill(start_color="FFA500", end_color="FFA500", fill_type="solid")
# green_fill = PatternFill(start_color="22e06e", end_color="22e06e", fill_type="solid")
# red_fill = PatternFill(start_color="FFFF0000", end_color="FFFF0000", fill_type="solid")
# # Создаем объект Alignment с выравниванием по центру
# center_alignment = Alignment(horizontal="center", vertical="center")
# # Создаем объект Border с обрамлением только для левой и правой сторон
# border = Border(
#     left=Side(style="thin"),
#     right=Side(style="thin"),
#     top=Side(style="thin"),
#     bottom=Side(style="thin"),
# )


# class Statistic:
#     def __init__(self):
#         self._table: dict[str, list] = defaultdict(list)
#         self._no_driver = defaultdict(int)
#         self._repair = defaultdict(int)
#         self._total = defaultdict(int)
#         self._titles: list[str] = []
#
#     @property
#     def no_driver(self) -> dict[str, int]:
#         return self._no_driver
#
#     @property
#     def repair(self) -> dict[str, int]:
#         return self._repair
#
#     @property
#     def total(self) -> dict[str, int]:
#         return self._total
#
#     @property
#     def table(self) -> dict[str, list]:
#         return self._table
#
#     @property
#     def titles(self) -> list[str]:
#         return self._titles
#
#
# class StatisticCalculator(Statistic):
#
#     def __init__(self, work_plan: dict[str, dict[str, str]]):
#         super().__init__()
#         self.work_plan = work_plan
#         self._calculate()
#
#     def _init_date(self, date: str):
#         self._no_driver[date] = 0
#         self._repair[date] = 0
#         self._total[date] = 0
#
#     def _init_static(self):
#         for date in self.work_plan:
#             self._init_date(date)
#
#     def _fill_table_data(self):
#         for date, car in self.work_plan.items():
#             for name, value in car.items():
#                 self.table[name].append(value)
#
#     def _fill_statistic(self):
#         for date, car in self.work_plan.items():
#             for name, value in car.items():
#                 if value == SIGNAL_WORK:
#                     self.no_driver[date] += 1
#                 elif value == SIGNAL_WEEKEND:
#                     self.repair[date] += 1
#                 else:
#                     self.total[date] += 1
#
#     def _fill_titles(self):
#         self._titles = ["    Машина    ", *[date for date in self.work_plan.keys()]]
#
#     def _calculate(self):
#         self._fill_table_data()
#         self._init_static()
#         self._fill_statistic()
#         self._fill_titles()
#
#
# class Excel:
#     def __init__(self, file):
#         self.file = file
#         self.wb = openpyxl.Workbook()
#         self.sheet = self.wb.active
#
#     def save(self):
#         self.wb.save(self.file)
#
#     def add_row(self, row: list[str]):
#         self.sheet.append(row)
#
#     def add_color_to_row_cells(self, row: int, colors: list[PatternFill]):
#         length = len(colors)
#         for index, cell in enumerate(self.sheet[row]):
#             if index >= length:
#                 break
#             elif fill := colors[index]:
#                 cell.fill = fill
#
#     def add_cell(self, row: int, column: int, value: str):
#         self.sheet.cell(row=row, column=column, value=value)
#
#     def auto_alignment_column_width(self):
#         for columns in self.sheet.iter_cols():
#             value = columns[0].value
#             length = len(str(value)) + str(value).count(" ") + 2
#             column_name = columns[0].column_letter
#             self.sheet.column_dimensions[column_name].width = length
#
#     def auto_alignment_column_center(self):
#         for columns in self.sheet.iter_cols():
#             for cell in columns:
#                 cell.alignment = center_alignment
#
#     def auto_border(self):
#         for columns in self.sheet.iter_cols():
#             for cell in columns:
#                 cell.border = border
#
#
# class CrewExel:
#
#     def __init__(self, excel: Excel, statistic: Statistic):
#         self.excel = excel
#         self.statistic = statistic
#
#     def create(self):
#         self.excel.add_row(self.statistic.titles)
#
#         for name, values in self.statistic.table.items():
#             self.excel.add_row([name, *values])
#
#         self.excel.add_row([])
#         self.make_sheet()
#         self.excel.save()
#
#     def make_sheet(self):
#         self.excel.add_color_to_row_cells(self.excel.sheet.max_row + 1,
#                                           [black_fill for _ in range(len(self.statistic.titles))])
#         self._add_statistic_row("без водителя", list(self.statistic.no_driver.values()))
#         self._add_statistic_row("в ремонте", list(self.statistic.repair.values()))
#         self._add_statistic_row("наряд", list(self.statistic.total.values()))
#
#     def _fill_color_to_row_cells(self, values: list[int]):
#         self.excel.add_color_to_row_cells(
#             self.excel.sheet.max_row,
#             [
#                 orange_fill,
#                 *[red_fill if value else green_fill for value in values],
#             ],
#
#         )
#
#     def _add_statistic_row(self, label: str, values: list[int]):
#         self.excel.add_row([label, *values])
#         self._fill_color_to_row_cells(values)


if __name__ == "__main__":
    from data import data

    excel_ = Excel("test_1.xlsx")
    static = StatisticCalculator(data)
    CrewExel(excel_, static).create()
