from store.ws.base.accessor import BaseAccessor
from store.ws.models import DriverModel


class DriverAccessor(BaseAccessor):
    class Meta:
        model = DriverModel
