from api.car.views import CarViews
from api.driver.views import DriverViews
from api.manager.views import ManagerViews
from api.schedule_type.views import ScheduleType
from api.work_schedule_history.views import WorkScheduleHistoryViews
from api.worker_schedule.views import WorkerScheduleViews
from fastapi import FastAPI


def setup_routes(app: FastAPI):
    """Настройка Роутов приложения."""
    # app.include_router(CarViews(prefix="/car", tags=["CAR"]))
    # app.include_router(DriverViews(prefix="/driver", tags=["DRIVER"]))
    # app.include_router(WorkScheduleHistoryViews(prefix="/work_schedule", tags=["WORK SCHEDULE HISTORY"]))
    app.include_router(ManagerViews(prefix="/resources", tags=["АКТИВЫ"]))
    app.include_router(ScheduleType(prefix="/schedule_type", tags=["SCHEDULE TYPE"]))

    app.include_router(
        WorkerScheduleViews(prefix="/worker_schedule", tags=["WORKER SCHEDULE"])
    )
