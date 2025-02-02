from datetime import datetime

from black.trans import defaultdict
from icecream import ic

from store.scheduler.employee_work_plan import EmployeeWorkPlan
from store.scheduler.worker_schedule import WorkerSchedule

date_format = "%Y-%m-%d"  # '%d-%m-%Y'

data = [
    # водитель
    (
        "Филатов Александр Алексеевич",
        [
            # список графиков за какой-то период,
            {
                # Начало периода
                "schedule_start_date": datetime.strptime("2025-01-20", date_format),
                "work_days": 4,
                "weekend_days": 2,
                "is_working": True,
                "what_day": 1,
            },
            {
                "schedule_start_date": datetime.strptime("2025-01-21", date_format),
                "work_days": 4,
                "weekend_days": 4,
                "is_working": False,
                "what_day": 2,
            },
        ],
    ),
    (
        "Миронов Михаил Викторович",
        [
            {
                "what_day": 3,
                "work_days": 4,
                "is_working": True,
                "weekend_days": 2,
                "schedule_start_date": datetime.strptime("2025-01-20", date_format),
            }
        ],
    ),
    (
        "Яшин Александр Кириллович",
        [
            {
                "what_day": 1,
                "work_days": 4,
                "is_working": False,
                "weekend_days": 2,
                "schedule_start_date": datetime.strptime("2025-01-20", date_format),
            },
            {
                "what_day": 3,
                "work_days": 4,
                "is_working": True,
                "weekend_days": 4,
                "schedule_start_date": datetime.strptime("2025-01-10", date_format),
            },
        ],
    ),
]

work_schedule_car_1 = WorkerSchedule(
    "Car_1",
    datetime(year=2025, month=1, day=1),
    work_days=-1,
    weekend_days=-1,
    is_working=True,
    what_day=1,
)
if __name__ == "__main__":
    # сортируем графики по дате начала
    for driver in data:
        driver[1].sort(key=lambda x: x["schedule_start_date"])

    employee = EmployeeWorkPlan(
        work_schedule_car_1,
    )
    new_1 = defaultdict(list)
    for name, schedules in data:
        new_1[name] = [WorkerSchedule(name, **schedule) for schedule in schedules]
    ic(new_1)
    # --------------------
    employee_1 = EmployeeWorkPlan(
        work_schedule_car_1,
        new_1["Филатов Александр Алексеевич"][0],
        new_1["Миронов Михаил Викторович"][0],
        new_1["Яшин Александр Кириллович"][0],
    )
    # ic(employee_1.get_schedule(datetime(2025, 1, 20), datetime(2025, 2, 20)))
    start = datetime(2025, 1, 20)
    end = datetime(2025, 1, 31)
    for a in zip(
        employee_1.get_schedule(start, end).items(),
        new_1["Филатов Александр Алексеевич"][0].make_schedule(start, end).items(),
        new_1["Миронов Михаил Викторович"][0].make_schedule(start, end).items(),
        new_1["Яшин Александр Кириллович"][0].make_schedule(start, end).items(),
        # employee_1.get_unused_employees(start, end).items(),
    ):
        print(
            a[0][0],
            a[0][1],
            a[1][1],
            a[2][1],
            a[3][1],
        )
    for a in employee_1.get_unused_employees(start, end).items():
        print(a)
