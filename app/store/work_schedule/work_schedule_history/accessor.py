from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import WorkScheduleHistoryModel


class WorkScheduleHistoryAccessor(BaseAccessor):
    class Meta:
        model = WorkScheduleHistoryModel
