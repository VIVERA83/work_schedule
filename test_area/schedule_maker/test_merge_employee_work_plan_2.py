from collections import defaultdict
from datetime import datetime

from icecream import ic

from test_area.schedule_maker.data import date_17_01_2025, today_1
from work_schedule.store.scheduler.combined_employees_work_plan import (
    CombinedEmployeesWorkPlan,
)
from work_schedule.store.scheduler.employee_work_plan import EmployeeWorkPlan
from work_schedule.store.scheduler.utils import SIGNAL_WEEKEND, SIGNAL_WORK
from work_schedule.store.scheduler.worker_schedule import WorkerSchedule


def merge_dict(d1: dict, d2: dict):
    unused = {
        date_1: {**values_1, **values_2}
        for (date_1, values_1), (date_2, values_2) in zip(d1.items(), d2.items())
    }
    return unused


def merge_employee_work_plan(
    employee_1: EmployeeWorkPlan, employee_2: EmployeeWorkPlan
):
    total = defaultdict(dict)
    unused = merge_dict(
        employee_1.get_unused_employees(), employee_2.get_unused_employees()
    )

    for (date_1, name_1), (date_2, name_2) in zip(
        employee_1.get_schedule().items(), employee_2.get_schedule().items()
    ):
        if name_1 != name_2:
            temp = {}
            # 1
            if name_1 in [SIGNAL_WEEKEND]:
                if today_unused := list(unused.get(date_1).keys()):
                    new_worker = today_unused[0]
                    temp.update({employee_1.name: name_1, employee_2.name: new_worker})
                    unused.get(date_1).pop(new_worker)
                else:
                    temp.update({employee_2.name: name_2})
            else:
                temp = {
                    employee_1.name: name_1,
                    employee_2.name: name_2,
                }
            total[date_1].update(temp)

        else:
            if name_1 in [SIGNAL_WEEKEND] and name_2 in [SIGNAL_WEEKEND]:
                total[date_1] = {
                    employee_1.name: name_1,
                    employee_2.name: name_2,
                }
            else:
                if data := list(unused.pop(date_1, {}).keys()):
                    total[date_1] = {
                        employee_1.name: name_1,
                        employee_2.name: data[-1],
                    }
                else:
                    total[date_1] = {
                        employee_1.name: name_1,
                        employee_2.name: SIGNAL_WORK,
                    }

        # удаление повторов
        removing_duplicates_from_unused(unused, total, date_1)
        # if data := unused.get(date_1):
        #     a = set(total[date_1].values())
        #     b = set(data.keys())
        #     if c := b - a:
        #         unused[date_1] = {
        #             element: unused[date_1][element]
        #             for element in c
        #         }
        #     elif a == b:
        #         unused[date_1] = {
        #             element: unused[date_1][element]
        #             for element in c
        #         }
        #     if not unused[date_1]:
        #         del unused[date_1]
    return total, unused


def removing_duplicates_from_unused(unused, total, date):
    if data := unused.get(date):
        a = set(total[date].values())
        b = set(data.keys())
        if c := b - a:
            unused[date] = {element: unused[date][element] for element in c}
        elif a == b:
            unused[date] = {element: unused[date][element] for element in c}
        if not unused[date]:
            del unused[date]


if __name__ == "__main__":
    work_schedule_driver_1 = WorkerSchedule(
        "driver_1",
        datetime(year=2025, month=1, day=1),
        work_days=4,
        weekend_days=4,
        is_working=True,
        what_day=1,
    )
    work_schedule_driver_2 = WorkerSchedule(
        "driver_2",
        datetime(year=2025, month=1, day=1),
        work_days=4,
        weekend_days=2,
        is_working=True,
        what_day=3,
    )
    work_schedule_driver_3 = WorkerSchedule(
        "driver_3",
        datetime(year=2025, month=1, day=1),
        work_days=4,
        weekend_days=4,
        is_working=False,
        what_day=1,
    )
    work_schedule_car_1 = WorkerSchedule(
        "Car_1",
        datetime(year=2025, month=1, day=1),
        work_days=5,
        weekend_days=2,
        is_working=True,
        what_day=2,
    )
    work_schedule_car_2 = WorkerSchedule(
        "Car_2",
        datetime(year=2025, month=1, day=1),
        work_days=5,
        weekend_days=2,
        is_working=True,
        what_day=2,
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

    result = CombinedEmployeesWorkPlan(employee_1, employee_2)

    # result = merge_employee_work_plan(employee_1, employee_2)
    # result.set_date(datetime(year=2025, month=1, day=1), datetime(year=2025, month=1, day=10))
    ic(result.get_schedule())
    # ic(result.get_unused_employees())
    ic(result.add_combined_employees_work_plan())

    iters = zip(
        work_schedule_driver_1.get_schedule(
            today_1,
            date_17_01_2025,
        ).values(),
        work_schedule_driver_2.get_schedule(
            today_1,
            date_17_01_2025,
        ).values(),
        work_schedule_driver_3.get_schedule(
            today_1,
            date_17_01_2025,
        ).values(),
        work_schedule_car_1.get_schedule(
            today_1,
            date_17_01_2025,
        ).values(),
        work_schedule_car_2.get_schedule(
            today_1,
            date_17_01_2025,
        ).values(),
    )
    [print(i) for i in iters]

    #  car_2 what_day=2 is_working=False
    a = {
        "11-01-2025": {"Car_1": "driver_2", "Car_2": "driver_3"},
        "12-01-2025": {"Car_1": "driver_2", "Car_2": "driver_3"},
        "13-01-2025": {"Car_1": "B", "Car_2": "driver_1"},
        "14-01-2025": {"Car_1": "B", "Car_2": "B"},
        "15-01-2025": {"Car_1": "driver_3", "Car_2": "B"},
        "16-01-2025": {"Car_1": "driver_3", "Car_2": "driver_1"},
        "17-01-2025": {"Car_1": "driver_3", "Car_2": "driver_2"},
    }

    b = {
        "13-01-2025": {"driver_2": "P"},
        "14-01-2025": {"driver_1": "P", "driver_2": "P"},
        "15-01-2025": {"driver_1": "P"},
    }

    # assert a == result.get_employee_work_plan()
    # assert b == result.get_unused_employees()

    a = {
        "11-01-2025": {"Car_1": "driver_2", "Car_2": "driver_3"},
        "12-01-2025": {"Car_1": "driver_2", "Car_2": "driver_3"},
        "13-01-2025": {"Car_1": "B", "Car_2": "driver_1"},
        "14-01-2025": {"Car_1": "B", "Car_2": "driver_1"},
        "15-01-2025": {"Car_1": "driver_3", "Car_2": "B"},
        "16-01-2025": {"Car_1": "driver_3", "Car_2": "B"},
        "17-01-2025": {"Car_1": "driver_3", "Car_2": "driver_2"},
    }

    b = {
        "13-01-2025": {"driver_2": "P"},
        "14-01-2025": {"driver_2": "P"},
        "15-01-2025": {"driver_1": "P"},
        "16-01-2025": {"driver_1": "P"},
    }
    # assert a == result[0]
    # assert b == result[1]
