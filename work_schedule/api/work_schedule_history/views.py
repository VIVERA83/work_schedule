from api.base.route import BaseRoute
from api.base.schemes import ID

from api.work_schedule_history.schemes import (
    WorkScheduleHistoryCreateSchema,
    WorkScheduleHistoryUpdateSchema,
    WorkScheduleHistorySchema,
)
from core.lifespan import db

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

work_schedule_history_route = BaseRoute(
    prefix="/work_schedule_history",
    tags=["WORK SCHEDULE HISTORY"],
    db=db.work_schedule_history,
    endpoints=endpoints,
)
