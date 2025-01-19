from api.base.route import BaseView
from api.base.schemes import ID
from api.work_schedule_history.schemes import (
    WorkScheduleHistoryCreateSchema,
    WorkScheduleHistorySchema,
    WorkScheduleHistoryUpdateSchema,
)
from core.lifespan import store


class WorkScheduleHistoryViews(BaseView):
    class Meta:
        db = store.work_schedule_history
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
                "response_model": WorkScheduleHistorySchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": WorkScheduleHistoryCreateSchema},
                "response_model": WorkScheduleHistorySchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
                "response_model": WorkScheduleHistorySchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": WorkScheduleHistoryUpdateSchema},
                "response_model": WorkScheduleHistorySchema,
            },
        }
