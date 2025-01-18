from api.base.route import BaseRoute
from api.base.schemes import ID
from api.schedule_type.schemes import (
    ScheduleTypeCreateSchema,
    ScheduleTypeSchema,
    ScheduleTypeUpdateSchema,
)
from core.lifespan import db

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

schedule_type_route = BaseRoute(
    prefix="/schedule_type",
    tags=["SCHEDULE TYPE"],
    db=db.schedule_type,
    endpoints=endpoints,
)
