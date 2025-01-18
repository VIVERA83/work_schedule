from store.ws.base.accessor import BaseAccessor
from store.ws.models import WorkScheduleHistoryModel


class WorkScheduleHistoryAccessor(BaseAccessor):
    class Meta:
        model = WorkScheduleHistoryModel
