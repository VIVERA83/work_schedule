from api.base.route import BaseView
from api.base.schemes import ID
from api.schedule_type.schemes import (
    ScheduleTypeCreateSchema,
    ScheduleTypeSchema,
    ScheduleTypeUpdateSchema,
)
from core.lifespan import store


class ScheduleType(BaseView):
    class Meta:
        store = store.schedule_type
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
                "response_model": ScheduleTypeSchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": ScheduleTypeCreateSchema},
                "response_model": ScheduleTypeSchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
                "response_model": ScheduleTypeSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": ScheduleTypeUpdateSchema},
                "response_model": ScheduleTypeSchema,
            },
        }
