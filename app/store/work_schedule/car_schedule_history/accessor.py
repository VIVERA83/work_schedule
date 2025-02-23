from store.work_schedule.base.accessor import BaseAccessor
from store.work_schedule.models import CarScheduleHistoryModel


class CarScheduleHistoryAccessor(BaseAccessor):
    class Meta:
        model = CarScheduleHistoryModel
