from store.ws.base.accessor import BaseAccessor
from store.ws.car.exceptions import CarDuplicateException
from store.ws.models import CarModel


class CarAccessor(BaseAccessor):
    class Meta:
        model = CarModel
        duplicate = CarDuplicateException
