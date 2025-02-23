from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import CrewModel


class CrewAccessor(BaseAccessor):
    class Meta:
        model = CrewModel
