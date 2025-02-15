from collections import defaultdict
from datetime import datetime

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
                "schedule_start_date": "2025-01-20T00:00:00",
            },
            {
                "what_day": 3,
                "work_days": 4,
                "is_working": True,
                "weekend_days": 4,
                "schedule_start_date": "2025-01-10T00:00:00",
            },
        ],
    ),
]

if __name__ == "__main__":
    WS = defaultdict(list)
    for name, schedule in data:
        for day in schedule:
            WS[name].append(WorkerSchedule(name, **day))
    ic(WS)
    workers = list(WS.keys())
    em = EmployeeWorkPlan(WS[workers[0]][0], WS[workers[1]][0])

    ic(em.get_schedule(datetime(2025, 1, 20), datetime(2025, 1, 31)))
