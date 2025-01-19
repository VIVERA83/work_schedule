from work_schedule.store.db.data.base import BaseDB
from work_schedule.store.db.data.dc import ScheduleType

data = [
    {
        "id": 0,
        "name": "4/2",
        "work_days": 4,
        "weekend_days": 2,
    },
    {
        "id": 1,
        "name": "4/4",
        "work_days": 4,
        "weekend_days": 4,
    },
]


class ScheduleTypeDB(BaseDB):
    """Типы графиков рабочего времени."""

    class Meta:
        db = data
        dataclass = ScheduleType
