from store.ws.base.accessor import BaseAccessor
from store.ws.models import ScheduleTypeModel


class ScheduleTypeAccessor(BaseAccessor):
    class Meta:
        model = ScheduleTypeModel
        ex = []
