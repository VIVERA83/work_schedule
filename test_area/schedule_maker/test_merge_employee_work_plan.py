from collections import defaultdict
from datetime import datetime

from icecream import ic

from test_area.schedule_maker.data import date_17_01_2025, today_1
from work_schedule.store.scheduler.employee_work_plan import EmployeeWorkPlan
from work_schedule.store.scheduler.utils import SIGNAL_WEEKEND, SIGNAL_WORK
from work_schedule.store.scheduler.worker_schedule import WorkerSchedule

ic.includeContext = True


def merge_dict_1(d1: dict, d2: dict):
    r = defaultdict(dict)
    # u = defaultdict(dict)
    for (
        (date_1, values_1),
        (date_2, values_2),
    ) in zip(d1.items(), d2.items()):
        if values_1 == values_2:
            r[date_1] = {"Car_1": values_1}
        else:
            if values_1 == SIGNAL_WEEKEND:
                r[date_1] = {"Car_2": values_2}

    return r


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
                    }

        # удаление повторов
        if data := unused.get(date_1):
            a = set(total[date_1].values())
            b = set(data.keys())
            # b = set(unused.get(date_1, {}).keys())
            if c := b - a:
                unused[date_1] = {element: unused[date_1][element] for element in c}
                # temp = {}
                # for element in c:
                #     temp.update({element: unused[date_1][element]})
                # unused[date_1] = temp
            elif a == b:
                unused[date_1] = {element: unused[date_1][element] for element in c}
                # temp = {}
                # for element in c:
                #     temp.update({element: unused[date_1][element]})
                # unused[date_1] = temp
            if not unused[date_1]:
                del unused[date_1]
    return total, unused


# def merge_employee_work_plan(employee_1: EmployeeWorkPlan, employee_2: EmployeeWorkPlan):
#     total = defaultdict(dict)
#     unused = merge_dict(employee_1.get_unused_employees(),employee_2.get_unused_employees())
#
#     # yesterday = list(employee_1.get_employee_work_plan().keys())[0]
#     for (date_1, name_1), (date_2, name_2) in zip(employee_1.get_employee_work_plan().items(),
#                                                   employee_2.get_employee_work_plan().items()):
#
#         if name_1 != name_2:
#             # if name_1 in [SIGNAL_WEEKEND] :
#
#             print(date_1, "else", name_1, unused.get(date_1))
#             total[date_1] = {
#                 employee_1.name: name_1,
#                 employee_2.name: name_2,
#             }
#         else:
#
#             if data := list(unused.pop(date_1, {}).keys()):
#                 total[date_1] = {
#                     employee_1.name: name_1,
#                     employee_2.name: data[-1],
#                 }
#             else:
#
#                 total[date_1] = {
#                     employee_1.name: name_1,
#
#                 }
#         # date_yesterday = total.get(yesterday)
#         # date_today = total.get(date_1)
#         # for name_yesterday, value_yesterday in date_yesterday.items():
#         #     for name_today, value_today in date_today.items():
#         #         if (name_yesterday == name_today):
#         #             date_yesterday[name_yesterday] = value_today
#         #             date_today[name_today] = value_yesterday
#         #             break
#
#         # yesterday = date_1
#     return total, unused


if __name__ == "__main__":
    work_schedule_driver_1 = WorkerSchedule(
        "driver_1",
        datetime(year=2025, month=1, day=1),
        work_days=4,
        weekend_days=2,
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
        weekend_days=2,
        is_working=False,
        what_day=1,
    )
    work_schedule_car_1 = WorkerSchedule(
        "Car_1",
        datetime(year=2025, month=1, day=1),
        work_days=5,
        weekend_days=2,
        is_working=True,
        what_day=1,
    )
    work_schedule_car_2 = WorkerSchedule(
        "Car_2",
        datetime(year=2025, month=1, day=1),
        work_days=5,
        weekend_days=2,
        is_working=False,
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
    result = merge_employee_work_plan(employee_1, employee_2)
    ic(result)
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
    )
    [print(i) for i in iters]
    # [print(a[0], a[1], b[1]) for a, b in zip(
    #     employee_1.get_unused_employees().items(),
    #     employee_2.get_unused_employees().items())
    #  ]
    print()

    # unused = {date_1: {**values_1, **values_2}
    # for (date_1, values_1), (date_2, values_2), in zip(employee_1.get_unused_employees().items(),
    #                                                    employee_2.get_unused_employees().items())
    # }
    # unused = merge_dict_1(employee_1.get_employee_work_plan(),
    #                       employee_2.get_employee_work_plan())

    # [print(i[0], i[1]) for i in unused.items()]
