from work_schedule.store.db.data.base import BaseDB
from work_schedule.store.db.data.dc import Car

data = [
    {
        "id": 0,
        "car_number": "А124МК196",
        "car_model": "MAN TGM",
    },
    {
        "id": 1,
        "car_number": "А777НН198",
        "car_model": "MAN TGS",
    }
]

class CarDB(BaseDB):
    class Meta:
        db = data
        dataclass = Car
