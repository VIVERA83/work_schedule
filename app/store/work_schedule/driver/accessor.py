from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import DriverModel


class DriverAccessor(BaseAccessor):
    class Meta:
        model = DriverModel
