from typing import Optional

from api.worker_schedule.schemes import ScheduleHistorySchema
from driver_scheduling.worker_schedule import Worker


def create_worker(
    name: str, schedules: list[ScheduleHistorySchema]
) -> Optional[Worker]:
    worker = None
    for schedule in schedules:
        if not worker:
            worker = Worker(
                name=name,
                schedule_start_date=schedule.schedule_start_date,
                work_days=schedule.work_days,
                weekend_days=schedule.weekend_days,
                is_working=schedule.is_working,
                what_day=schedule.what_day,
            )
        else:
            worker.add_worker_schedule(
                schedule_start_date=schedule.schedule_start_date,
                work_days=schedule.work_days,
                weekend_days=schedule.weekend_days,
                is_working=schedule.is_working,
                what_day=schedule.what_day,
            )
    return worker


# теперь экипажи преобразовать в CombinedEmployeesWorkPlan (Объединенный график работы сотрудников на оборудовании.)
#         combined_employees_work_plans = {}
#
# class AnyManagerSchedule:
#
#         def __init__(self, schedules: list[ScheduleHistorySchema]):
#
#         for crew_id, crew in dict_crews.items():
#             car_workers = []
#             driver_workers = []
#
#             for car in crew.cars:
#
#                 if car.schedules:
#                     if car.schedules[0].schedule_start_date > start_date:
#                         car.schedules.insert(0, ScheduleHistorySchema(
#                             schedule_start_date=start_date,
#                             work_days=-1,
#                             weekend_days=-1,
#                             is_working=True,
#                             what_day=0,
#                         )
#                                              )
#                 car_workers.append(create_worker(car.number, car.schedules))
#
#             for driver in crew.drivers:
#                 if driver.schedules:
#                     if driver.schedules[0].schedule_start_date > start_date:
#                         driver.schedules.insert(0, ScheduleHistorySchema(
#                             schedule_start_date=start_date,
#                             work_days=-1,
#                             weekend_days=-1,
#                             is_working=True,
#                             what_day=0,
#                         )
#                                                 )
#                 driver_workers.append(create_worker(driver.name, driver.schedules))
#
#             employee_work_plans = []
#             for car_worker in car_workers:
#                 if car_worker is not None:
#                     ic(car_worker, driver_workers)
#                     employee_work_plans.append(EmployeeWorkPlan(car_worker, *driver_workers))
#
#             # try:
#             if employee_work_plans:
#                 combined_employees_work_plans[crew_id] = CombinedEmployeesWorkPlan(*employee_work_plans)
#             # except Exception as e:
#             #     print(e)
#             ic(car_workers)
#             ic(driver_workers)
#             ic(employee_work_plans)
#             ic(combined_employees_work_plans)
