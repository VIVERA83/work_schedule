import logging

from api.car.views import CarViews
from api.car_schedule_history.views import CarScheduleHistoryViews
from api.driver.views import DriverViews
from api.manager.views import ManagerViews
from api.schedule_type.views import ScheduleType
from api.work_schedule_history.views import WorkScheduleHistoryViews
from api.worker_schedule.views import WorkerScheduleViews
from fastapi import FastAPI


def setup_routes(app: FastAPI, logger: logging.Logger):
    """Настройка Роутов приложения."""
    app.include_router(CarViews(prefix="/car", tags=["CAR"], logger=logger))
    app.include_router(DriverViews(prefix="/driver", tags=["DRIVER"], logger=logger))
    app.include_router(
        WorkScheduleHistoryViews(
            prefix="/work_schedule_history",
            tags=["WORK SCHEDULE HISTORY"],
            logger=logger,
        )
    )
    app.include_router(
        ScheduleType(prefix="/schedule_type", tags=["SCHEDULE TYPE"], logger=logger)
    )

    app.include_router(
        WorkerScheduleViews(
            prefix="/worker_schedule", tags=["WORKER SCHEDULE"], logger=logger
        )
    )
    app.include_router(
        CarScheduleHistoryViews(
            prefix="/car_schedule_history", tags=["CAR SCHEDULE HISTORY"], logger=logger
        )
    )
    app.include_router(
        ManagerViews(prefix="/resources", tags=["АКТИВЫ"], logger=logger)
    )
