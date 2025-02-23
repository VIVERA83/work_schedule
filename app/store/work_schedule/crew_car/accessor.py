from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import  CrewDriverModel


class CrewDriverAccessor(BaseAccessor):
    class Meta:
        model = CrewDriverModel
