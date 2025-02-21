from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.car.exceptions import CarDuplicateException
from store.work_schedule.models import CarModel


class CarAccessor(BaseAccessor):
    class Meta:
        model = CarModel
        duplicate = CarDuplicateException
