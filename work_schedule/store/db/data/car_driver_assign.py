from work_schedule.store.db.data.base import BaseDB
from work_schedule.store.db.data.dc import CarDriverAssign

data = [
    {
        "id": 0,
        "id_car": 0,
        "id_driver": 0,
    },
    {
        "id": 1,
        "id_car": 1,
        "id_driver": 1,
    },
]


class CarDriverAssignDB(BaseDB):
    """Закрепление автомобиля к водителю."""

    class Meta:
        db = data
        dataclass = CarDriverAssign
