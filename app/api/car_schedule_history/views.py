from api.base.route import BaseView
from api.base.schemes import ID_PATH
from api.car_schedule_history.schemes import (
    CarScheduleHistoryCreateSchema,
    CarScheduleHistorySchema,
    CarScheduleHistoryUpdateSchema,
)


from core.lifespan import store


class CarScheduleHistoryViews(BaseView):
    class Meta:
        store = store.car_schedule_history
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "response_model": CarScheduleHistorySchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CarScheduleHistoryCreateSchema},
                "response_model": CarScheduleHistorySchema,
                "summary": "Назначить график работы машины",
                "description": "Назначить график работы машины.<br><br>"
                "`id_car` - идентификатор машины<br>"
                "`id_schedule_type` - идентификатор типа расписания<br>"
                "`date` - дата начала графика<br>"
                "`is_working` - флаг работы машины(день ППО или ППР)<br>"
                "`what_day` - Который день, машина работает(отдыхает)<br><br>"
                "После назначения графика работы машины становится доступным для включения в наряд.",
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID_PATH},
                "response_model": CarScheduleHistorySchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": CarScheduleHistoryUpdateSchema},
                "response_model": CarScheduleHistorySchema,
            },
        }
