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
        store = store.work_schedule_history
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
                "summary": "Назначить график работы водителю",
                "description": "Назначить график работы водителю.<br><br>"
                "`id_driver` - идентификатор водителя<br>"
                "`id_schedule_type` - идентификатор типа расписания<br>"
                "`date` - дата начала графика<br>"
                "`is_working` - флаг работы водителя(выходной или рабочий день)<br>"
                "`what_day` - Который день, водитель работает(отдыхает)<br><br>"
                "После назначения графика работы водитель становится доступным для включения в наряд.",
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
