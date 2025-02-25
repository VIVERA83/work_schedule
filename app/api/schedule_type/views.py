from api.base.route import BaseView
from api.base.schemes import ID_PATH
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
                "annotations": {"id_": ID_PATH},
                "response_model": ScheduleTypeSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": ScheduleTypeUpdateSchema},
                "response_model": ScheduleTypeSchema,
            },
        }
