from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import ScheduleTypeModel


class ScheduleTypeAccessor(BaseAccessor):
    class Meta:
        model = ScheduleTypeModel
