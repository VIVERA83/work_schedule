from datetime import datetime

from icecream import ic

from tests.schedule_maker.data import today_1, date_17_01_2025
from tests.schedule_maker.test_combined_empoyees_work_plan import employee_3, employee_4
from work_schedule.store.scheduler.combined_employees_work_plan import CombinedEmployeesWorkPlan
from work_schedule.store.scheduler.employee_work_plan import EmployeeWorkPlan
from work_schedule.store.scheduler.schedule_manager import ScheduleManager
from work_schedule.store.scheduler.worker_schedule import WorkerSchedule

work_schedule_driver_1 = WorkerSchedule("driver_1",
                                        datetime(year=2025, month=1, day=1),
                                        work_days=4,
                                        weekend_days=4,
                                        is_working=True,
                                        what_day=1,
                                        )
work_schedule_driver_2 = WorkerSchedule("driver_2",
                                        datetime(year=2025, month=1, day=1),
                                        work_days=4,
                                        weekend_days=2,
                                        is_working=True,
                                        what_day=3,
                                        )
work_schedule_driver_3 = WorkerSchedule("driver_3",
                                        datetime(year=2025, month=1, day=1),
                                        work_days=4,
                                        weekend_days=4,
                                        is_working=False,
                                        what_day=1,
                                        )
work_schedule_car_1 = WorkerSchedule("Car_1",
                                     datetime(year=2025, month=1, day=1),
                                     work_days=5,
                                     weekend_days=2,
                                     is_working=True,
                                     what_day=2,
                                     )
work_schedule_car_2 = WorkerSchedule("Car_2",
                                     datetime(year=2025, month=1, day=1),
                                     work_days=5,
                                     weekend_days=2,
                                     is_working=True,
                                     what_day=2
                                     )
employee_1 = EmployeeWorkPlan(
    work_schedule_car_1,
    work_schedule_driver_1,
    work_schedule_driver_2,
    work_schedule_driver_3,
)
employee_2 = EmployeeWorkPlan(
    work_schedule_car_2,
    work_schedule_driver_1,
    work_schedule_driver_2,
    work_schedule_driver_3,
)

if __name__ == '__main__':
    combined_employees_work_plan_1 = CombinedEmployeesWorkPlan(employee_1, employee_2)
    combined_employees_work_plan_2 = CombinedEmployeesWorkPlan(employee_3, employee_4)
    manager = ScheduleManager()
    manager.add_combined_employees_work_plan(combined_employees_work_plan_1)
    manager.add_combined_employees_work_plan(combined_employees_work_plan_2)
    schedule = manager.get_schedule(end=date_17_01_2025)
    ic(schedule)
