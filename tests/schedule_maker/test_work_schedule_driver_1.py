# from collections import defaultdict
# from datetime import datetime
#
# from work_schedule.store.scheduler.schedule_maker import ScheduleMaker
# from work_schedule.store.scheduler.utils import SIGNAL_WORK
#
#
# def test_schedule_version_4(start: datetime, end: datetime, *schedule_makers: ScheduleMaker):
#     # self
#     base_schedule_maker = ScheduleMaker(
#         "Car",
#         datetime(year=2025, month=1, day=1),
#         5,
#         2,
#         True,
#         1,
#     )
#     # тоже self
#     test_scheduler_car = base_schedule_maker.make_schedule_generator(start, end)
#
#
#     gens = {schedule_maker.name: schedule_maker.make_schedule_generator(start, end) for schedule_maker in
#             schedule_makers}
#     current_id = list(gens.keys())[0]
#     current_index = 0
#     date = None
#     table = {}
#     buffer = defaultdict(dict)
#
#     while True:
#         try:
#             car_date, car_signal = next(test_scheduler_car)
#
#             if car_signal == SIGNAL_WORK:
#
#                 for index, (id_, gen) in enumerate(gens.items()):
#                     date, signal = next(gen)
#
#                     if current_id == id_ and signal == SIGNAL_WORK:
#                         table[date] = current_id
#                         current_index = index
#                     elif signal == SIGNAL_WORK:
#                         buffer[date][id_] = signal
#
#                 if table.get(date, None) is None:
#                     if buffer_data := buffer.get(date, None):
#
#                         indexs = {list(gens.keys()).index(id_): [id_, s] for id_, s in buffer_data.items()}
#
#                         for ind, (id_, s) in indexs.items():
#
#                             if ind > current_index:
#                                 current_id = id_
#                                 break
#
#                         if buffer_data.get(current_id, None) is None:
#                             current_id = indexs[list(indexs.keys())[0]][0]
#                         buffer_data.pop(current_id)
#                         table[date] = current_id
#
#                         if not buffer.get(date, None):
#                             buffer.pop(date)
#
#                     else:
#                         table[car_date] = car_signal
#             else:
#                 table[car_date] = car_signal
#                 for index, (id_, gen) in enumerate(gens.items()):
#                     date, signal = next(gen)
#                     if signal == SIGNAL_WORK:
#                         buffer[date][id_] = signal
#         except StopIteration:
#             break
#     return table, buffer
from datetime import datetime

from icecream import ic

from tests.schedule_maker.data import today_1, date_17_01_2025, driver_0_s, driver_1_s, driver_2_s
from work_schedule.store.scheduler.employee_scheduling_diagrams import EmployeeWorkPlan
from work_schedule.store.scheduler.schedule_maker import WorkerSchedule

if __name__ == '__main__':
    driver_1 =WorkerSchedule("driver_1",
                         datetime(year=2025, month=1, day=1),
                           work_days=4,
                           weekend_days=2,
                           is_working=True,
                           what_day=1,
                         )
    driver_2 =WorkerSchedule("driver_2",
                         datetime(year=2025, month=1, day=1),
                           work_days=4,
                           weekend_days=2,
                           is_working=True,
                           what_day=3,
                         )
    driver_3 =WorkerSchedule("driver_3",
                         datetime(year=2025, month=1, day=1),
                           work_days=4,
                           weekend_days=2,
                           is_working=False,
                           what_day=1,
                         )
    car_1 = WorkerSchedule("Car_1",
                         datetime(year=2025, month=1, day=1),
                           work_days=5,
                           weekend_days=2,
                           is_working=True,
                           what_day=1,
                         )
    car_2 = WorkerSchedule("Car_2",
                           datetime(year=2025, month=1, day=1),
                           work_days=-1,
                           weekend_days=-1,
                           is_working=True,
                           what_day=1,
                           )
    employee_1 = EmployeeWorkPlan(
        today_1,
        date_17_01_2025,
        car_1,
        driver_1,
        driver_2,
        driver_3,
    )
    employee_2 = EmployeeWorkPlan(
        today_1,
        date_17_01_2025,
        car_2,
        driver_2,
        driver_3,
        driver_1,
    )
    # for d_1, d_2 in zip(employee_1.get_employee_work_plan().items(), employee_2.get_employee_work_plan().items()):
    #     print(d_1[0], d_1[1], d_2[1])
    [print(k[0], k[1], v[1]) for k, v in zip(employee_1.get_unused_employees().items(), employee_1.get_unused_employees().items())]

    # ic(employee_1.get_unused_employees())
    # ic(employee_2.get_unused_employees())
    a = employee_1.merger(employee_2)
    ic(a)


    # table, buffers = car.test_schedule_version_4(today_1, date_17_01_2025, driver_0_s, driver_1_s)
    # print(*(f"{k} : {v}" for k, v in table.items()), sep='\n')
    # print()
    # print(*(f"{k} : {v}" for k, v in buffers.items()), sep='\n')