from work_schedule.store.db.data.base import BaseDB
from work_schedule.store.db.data.dc import Driver

data = [
    {
        "id": 0,
        "name": "Иванов Иван Иванович",
    },
    {
        "id": 1,
        "name": "Сидоров Сидор Сидорович",
    }
]


class DriverDB(BaseDB):
    class Meta:
        db = data
        dataclass = Driver
