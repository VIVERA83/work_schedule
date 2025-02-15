from collections import defaultdict

from icecream import ic

from test_area.schedule_maker.data import date_06_01_2025, date_17_01_2025
from test_area.schedule_maker.test_combined_empoyees_work_plan import employee_3, employee_4
from test_area.schedule_maker.test_shedule_manager.test_shedule_manager import (
    employee_1,
    employee_2,
)
from work_schedule.store.excel.excel import Excel
from work_schedule.store.excel.utils import (
    black_fill,
    green_fill,
    orange_fill,
    red_fill,
)
from work_schedule.store.scheduler.combined_employees_work_plan import (
    CombinedEmployeesWorkPlan,
)
from work_schedule.store.scheduler.schedule_manager import ScheduleManager
from work_schedule.store.scheduler.utils import SIGNAL_WEEKEND, SIGNAL_WORK

ic.includeContext = True
combined_employees_work_plan_1 = CombinedEmployeesWorkPlan(employee_1, employee_2)
combined_employees_work_plan_2 = CombinedEmployeesWorkPlan(employee_3, employee_4)

if __name__ == "__main__":
    excel = Excel("test.xlsx")
    manager = ScheduleManager()

    manager.add_combined_employees_work_plan(combined_employees_work_plan_1)
    manager.add_combined_employees_work_plan(combined_employees_work_plan_2)
    data = manager.get_schedule(date_06_01_2025, date_17_01_2025)
    # ic(data)
    # 1 строка
    title = ["    Машина    ", *[date for date in data.keys()]]
    excel.add_row(title)
    # 2 строки с данными
    car_rows: dict[str, list] = defaultdict(list)
    statistic: dict[str, dict[str, int]] = defaultdict(dict)
    statistic["Машина без водителя"] = defaultdict(int)
    statistic["Машина в ремонте"] = defaultdict(int)
    statistic["Общий наряд"] = defaultdict(int)
    for date, car in data.items():
        for name, data in statistic.items():
            data[date] = 0

        for name, value in car.items():
            car_rows[name].append(value)
            if value == SIGNAL_WORK:
                statistic["Машина без водителя"][date] += 1
            elif value == SIGNAL_WEEKEND:
                statistic["Машина в ремонте"][date] += 1
            else:
                statistic["Общий наряд"][date] += 1

    ic(statistic)
    for name, values in car_rows.items():
        excel.add_row([name, *values])
    # 3 служебная информация
    excel.add_row([])
    excel.add_color_to_row_cells(
        excel.sheet.max_row + 1, [black_fill for _ in range(len(title))]
    )
    for name, values in statistic.items():
        excel.add_row([name, *values.values()])
        excel.add_color_to_row_cells(
            excel.sheet.max_row,
            [
                orange_fill,
                *[red_fill if value else green_fill for value in values.values()],
            ],
        )

    # сохранение

    excel.auto_alignment_column_center()
    excel.auto_alignment_column_width()
    excel.save()
