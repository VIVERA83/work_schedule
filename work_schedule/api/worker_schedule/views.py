from collections import defaultdict
from datetime import datetime

from icecream import ic

from api.base.route import BaseView
from api.worker_schedule.schemes import (
    WorkerScheduleCreateSchema,
    WorkerScheduleSchema,
    CrewSchema, ScheduleHistorySchema,
)
from api.worker_schedule.utils import create_worker
from core.lifespan import store
from store.excel.excel import Excel
from store.excel.utils import black_fill, orange_fill, red_fill, green_fill
from store.scheduler.combined_employees_work_plan import CombinedEmployeesWorkPlan
from store.scheduler.employee_work_plan import EmployeeWorkPlan
from store.scheduler.schedule_manager import ScheduleManager
from store.scheduler.utils import SIGNAL_WORK, SIGNAL_WEEKEND
from store.scheduler.worker_schedule import Worker
from store.store import Store
from test_area.schedule_maker.test_shedule_manager.test_excel.test_excel import combined_employees_work_plan_2
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
        date_2025_01_01 = datetime(2025, 1, 1)
        date_2025_01_10 = datetime(2025, 1, 10)

        # Получаем список экипажей с графиками работы в указанный диапазон времени
        row_crews = await self.db.manager.get_all_crews(start_date, end_date)
        # Преобразовали список в словарь экипажей, ключ = id экипажа, моделей Pydantic
        dict_crews = {
            item[0]: CrewSchema(id=item[0], cars=item[1], drivers=item[2]) for item in row_crews
        }
        ic(dict_crews)
        # теперь экипажи преобразовать в CombinedEmployeesWorkPlan (Объединенный график работы сотрудников на оборудовании.)
        combined_employees_work_plans = {}

        for crew_id, crew in dict_crews.items():
            car_workers = []
            driver_workers = []

            for car in crew.cars:

                if car.schedules:
                    if car.schedules[0].schedule_start_date > date_2025_01_01:
                        car.schedules.insert(0,ScheduleHistorySchema(
                            schedule_start_date=date_2025_01_01,
                            work_days=-1,
                            weekend_days=-1,
                            is_working=True,
                            what_day=0,
                        )
                                             )
                car_workers.append(create_worker(car.number, car.schedules))

            for driver in crew.drivers:
                if driver.schedules:
                    if driver.schedules[0].schedule_start_date > date_2025_01_01:
                        driver.schedules.insert(0,ScheduleHistorySchema(
                            schedule_start_date=date_2025_01_01,
                            work_days=-1,
                            weekend_days=-1,
                            is_working=True,
                            what_day=0,
                        )
                               )
                driver_workers.append(create_worker(driver.name, driver.schedules))

            employee_work_plans = []
            for car_worker in car_workers:
                ic(car_worker.name, driver_workers)
                employee_work_plans.append(EmployeeWorkPlan(car_worker, *driver_workers))

            # try:

            combined_employees_work_plans[crew_id] = CombinedEmployeesWorkPlan(*employee_work_plans)
            # except Exception as e:
            #     print(e)
            ic(car_workers)
            ic(driver_workers)
            ic(employee_work_plans)
            ic(combined_employees_work_plans)

        # # ===================
        crews = [CrewSchema(id=item[0], cars=item[1], drivers=item[2]) for item in row_crews]
        # # ic(crews)
        #
        #
        #
        #
        # car_workers = []
        # driver_workers = []
        # for crew in crews:
        #     # ic(crew)
        #     for car in crew.cars:
        #         if car.schedules:
        #             for index, schedule in enumerate(car.schedules):
        #                 if not index:
        #                     worker = Worker(name=car.number,
        #                                     schedule_start_date=schedule.schedule_start_date,
        #                                     work_days=schedule.work_days,
        #                                     weekend_days=schedule.weekend_days,
        #                                     is_working=schedule.is_working,
        #                                     what_day=schedule.what_day,
        #                                     )
        #                 else:
        #                     worker.add_worker_schedule(schedule.schedule_start_date, schedule.work_days,
        #                                                schedule.weekend_days, schedule.is_working, schedule.what_day)
        #             car_workers.append(worker)
        #
        #     for driver in crew.drivers:
        #         if driver.schedules:
        #             for index, schedule in enumerate(driver.schedules):
        #                 if not index:
        #                     worker = Worker(name=driver.name,
        #                                     schedule_start_date=schedule.schedule_start_date,
        #                                     work_days=schedule.work_days,
        #                                     weekend_days=schedule.weekend_days,
        #                                     is_working=schedule.is_working,
        #                                     what_day=schedule.what_day,
        #                                     )
        #                 else:
        #                     worker.add_worker_schedule(schedule.schedule_start_date, schedule.work_days,
        #                                                schedule.weekend_days, schedule.is_working, schedule.what_day)
        #             driver_workers.append(worker)
        #
        # employee_car_1 = EmployeeWorkPlan(car_workers[0], *driver_workers)
        # employee_car_2 = EmployeeWorkPlan(car_workers[1], *driver_workers)
        #
        # # ic(employee_car_1, employee_car_2)
        # # ic(car_workers)
        # comb = CombinedEmployeesWorkPlan(employee_car_1, employee_car_2)
        # comb_1 = CombinedEmployeesWorkPlan(employee_car_2, employee_car_1)
        # # ic(comb.get_schedule(date_2025_01_01, date_2025_01_10))
        # # ic()
        # теперь все засунуть в excel
        excel = Excel("test.xlsx")
        manager = ScheduleManager()

        for combined_employees_work_plan in combined_employees_work_plans.values():
            ic(combined_employees_work_plan)
            manager.add_combined_employees_work_plan(combined_employees_work_plan)
        # а если еще
        # manager.add_combined_employees_work_plan(combined_employees_work_plan_2)

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

        # ic(statistic)
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
