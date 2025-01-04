from datetime import datetime

from work_schedule.store.db.data.base import BaseDB
from work_schedule.store.db.data.dc import WorkScheduleHistory

data = [
    {
        "id": 0,
        "id_driver": 0,
        "id_schedule_type": 0,
        "date": datetime.now(),
        "is_working": False,
        "what_day": 1,
    },
    {
        "id": 0,
        "id_driver": 1,
        "id_schedule_type": 0,
        "date": datetime.now(),
        "is_working": True,
        "what_day": 1,
    },
]




class WorkScheduleHistoryDB(BaseDB):
    class Meta:
        db = data
        dataclass = WorkScheduleHistory
