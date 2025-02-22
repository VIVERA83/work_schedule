from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import CrewCarsModel


class CrewCarAccessor(BaseAccessor):
    class Meta:
        model = CrewCarsModel
