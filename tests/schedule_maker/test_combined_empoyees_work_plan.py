from datetime import datetime

from icecream import ic

from tests.schedule_maker.data import today_1, date_17_01_2025
from work_schedule.store.scheduler.combined_employees_work_plan import CombinedEmployeesWorkPlan
from work_schedule.store.scheduler.employee_work_plan import EmployeeWorkPlan
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
    today_1,
    date_17_01_2025,
    work_schedule_car_1,
    work_schedule_driver_1,
    work_schedule_driver_2,
    work_schedule_driver_3,
)
employee_2 = EmployeeWorkPlan(
    today_1,
    date_17_01_2025,
    work_schedule_car_2,
    work_schedule_driver_1,
    work_schedule_driver_2,
    work_schedule_driver_3,
)

work_schedule_driver_4 = WorkerSchedule("driver_4",
                                        datetime(year=2025, month=1, day=1),
                                        work_days=6,
                                        weekend_days=3,
                                        is_working=True,
                                        what_day=1,
                                        )
work_schedule_driver_5 = WorkerSchedule("driver_5",
                                        datetime(year=2025, month=1, day=1),
                                        work_days=6,
                                        weekend_days=3,
                                        is_working=True,
                                        what_day=3,
                                        )
work_schedule_driver_6 = WorkerSchedule("driver_6",
                                        datetime(year=2025, month=1, day=1),
                                        work_days=6,
                                        weekend_days=3,
                                        is_working=False,
                                        what_day=1,
                                        )
work_schedule_car_3 = WorkerSchedule("Car_3",
                                     datetime(year=2025, month=1, day=1),
                                     work_days=-1,
                                     weekend_days=-1,
                                     is_working=True,
                                     what_day=1,
                                     )
work_schedule_car_4 = WorkerSchedule("Car_4",
                                     datetime(year=2025, month=1, day=1),
                                     work_days=-1,
                                     weekend_days=-1,
                                     is_working=True,
                                     what_day=1
                                     )
employee_3 = EmployeeWorkPlan(
    # today_1,
    # date_17_01_2025,
    work_schedule_car_3,
    work_schedule_driver_4,
    # work_schedule_driver_5,
    work_schedule_driver_6,
)
employee_4 = EmployeeWorkPlan(
    # today_1,
    # date_17_01_2025,
    work_schedule_car_4,
    work_schedule_driver_4,
    # work_schedule_driver_5,
    work_schedule_driver_6,
)

if __name__ == '__main__':
    combined_employees_work_plan_1 = CombinedEmployeesWorkPlan(employee_1, employee_2)
    combined_employees_work_plan_2 = CombinedEmployeesWorkPlan(employee_3, employee_4)
    # ic(combined_employees_work_plan_2.get_employee_work_plan())
    # ic(combined_employees_work_plan_2.get_unused_employees())
    # iters = zip(work_schedule_driver_4.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_driver_5.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_driver_6.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_car_3.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_car_4.make_schedule(today_1, date_17_01_2025, ).values(),
    #             )
    # [print(i, i[:3].count("B"), i[3:].count("B"), i[:3].count("P"),  i[3:].count("P")) for i in iters]

    # iters = zip(work_schedule_driver_1.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_driver_2.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_driver_3.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_car_1.make_schedule(today_1, date_17_01_2025, ).values(),
    #             work_schedule_car_2.make_schedule(today_1, date_17_01_2025, ).values(),
    #             )
    # ic(combined_employees_work_plan_1.get_employee_work_plan())
    # ic(combined_employees_work_plan_1.get_unused_employees())
    # [print(i, i[:3].count("B"), i[3:].count("B"), i[:3].count("P"),  i[3:].count("P")) for i in iters]
    # ic(combined_employees_work_plan_1.get_unused_employees())
    # ic(work_schedule_driver_4.make_schedule(today_1, date_17_01_2025, ))
    # ic(work_schedule_driver_5.make_schedule(today_1, date_17_01_2025, ))
    # ic(work_schedule_driver_6.make_schedule(today_1, date_17_01_2025, ))
    print(combined_employees_work_plan_1.get_unused_employees())
    print(combined_employees_work_plan_2.get_unused_employees())
    used, not_used = combined_employees_work_plan_1.add_combined_employees_work_plan(combined_employees_work_plan_2)
    ic(used)
    ic(not_used)

