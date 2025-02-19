from collections import defaultdict
from datetime import datetime

from icecream import ic

from api.base.route import BaseView
from api.worker_schedule.schemes import (
    WorkerScheduleCreateSchema,
    WorkerScheduleSchema,
    CrewSchema,
)
from core.lifespan import store
from store.excel.excel import Excel
from store.excel.utils import black_fill, orange_fill, red_fill, green_fill
from store.scheduler.combined_employees_work_plan import CombinedEmployeesWorkPlan
from store.scheduler.employee_work_plan import EmployeeWorkPlan
from store.scheduler.schedule_manager import ScheduleManager
from store.scheduler.utils import SIGNAL_WORK, SIGNAL_WEEKEND
from store.scheduler.worker_schedule import Worker
from store.store import Store
from test_area.schedule_maker.test_shedule_manager.test_shedule_manager import employee_1


class WorkerScheduleViews(BaseView):
    db: Store

    class Meta:
        db = store
        endpoints = {
            "get_worker_schedule": {
                "methods": ["POST"],
                "annotations": {"data": WorkerScheduleCreateSchema},
                "response_model": WorkerScheduleSchema,
                "path": "/get_driver_schedule",
                "summary": "Получить график водителя",
                "description": "получение данных для построения графика графика работы водителя.",
            },
            "get_all_crews": {
                "methods": ["GET"],
                "path": "/get_all_crews",
                "response_model": list[CrewSchema],
                "summary": "Получить список экипажей",
                "description": "Получить список экипажей с графиками работы в указанный диапазон времени",
            },
        }

    async def get_worker_schedule(self, data: WorkerScheduleCreateSchema):
        return await self.db.manage_worker_schedule.get_worker_schedule(
            **data.model_dump()
        )

    async def get_all_crews(
            self,
            start_date: datetime = datetime.now(),
            end_date: datetime = datetime.now(),
    ):
        row_crews = await self.db.manager.get_all_crews(start_date, end_date)
        crews = [CrewSchema(id=item[0], cars=item[1], drivers=item[2]) for item in row_crews]
        ic(crews)

        date_2025_01_01 = datetime(2025, 1, 1)
        date_2025_01_10 = datetime(2025, 1, 10)

        car_workers = []
        driver_workers = []
        for crew in crews:

            for car in crew.cars:
                if car.schedules:
                    for index, schedule in enumerate(car.schedules):
                        if not index:
                            worker = Worker(name=car.number,
                                            schedule_start_date=schedule.schedule_start_date,
                                            work_days=schedule.work_days,
                                            weekend_days=schedule.weekend_days,
                                            is_working=schedule.is_working,
                                            what_day=schedule.what_day,
                                            )
                        else:
                            worker.add_worker_schedule(schedule.schedule_start_date, schedule.work_days,
                                                       schedule.weekend_days, schedule.is_working, schedule.what_day)
                    car_workers.append(worker)

            for driver in crew.drivers:
                if driver.schedules:
                    for index, schedule in enumerate(driver.schedules):
                        if not index:
                            worker = Worker(name=driver.name,
                                        schedule_start_date=schedule.schedule_start_date,
                                        work_days=schedule.work_days,
                                        weekend_days=schedule.weekend_days,
                                        is_working=schedule.is_working,
                                        what_day=schedule.what_day,
                                        )
                        else:
                            worker.add_worker_schedule(schedule.schedule_start_date, schedule.work_days,
                                                    schedule.weekend_days, schedule.is_working, schedule.what_day)
                    driver_workers.append(worker)


        employee_car_1 = EmployeeWorkPlan(car_workers[0], *driver_workers)
        employee_car_2 = EmployeeWorkPlan(car_workers[1], *driver_workers)

        ic(employee_car_1, employee_car_2)
        comb = CombinedEmployeesWorkPlan(employee_car_1, employee_car_2)
        comb_1 = CombinedEmployeesWorkPlan(employee_car_2, employee_car_1)
        ic(comb.get_schedule(date_2025_01_01, date_2025_01_10))
        ic()
        # теперь все засунуть в excel
        excel = Excel("test.xlsx")
        manager = ScheduleManager()

        manager.add_combined_employees_work_plan(comb)
        # manager.add_employee_work_plan(comb_1)

        data = manager.get_schedule(date_2025_01_01, date_2025_01_10)
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

        return crews
