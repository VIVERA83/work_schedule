from tests.schedule_maker.data import date_06_01_2025
from work_schedule.store.db.data.base import BaseDB
from work_schedule.store.db.data.dc import WorkScheduleHistory

data = [
    {
        "id": 0,
        "id_driver": 0,
        "id_schedule_type": 0,
        "date": date_06_01_2025,
        "is_working": False,
        "what_day": 1,
    },
    {
        "id": 1,
        "id_driver": 1,
        "id_schedule_type": 0,
        "date": date_06_01_2025,
        "is_working": True,
        "what_day": 4,
    },
]




class WorkScheduleHistoryDB(BaseDB):
    class Meta:
        db = data
        dataclass = WorkScheduleHistory
