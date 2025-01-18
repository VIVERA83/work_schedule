from api.car.views import car_route
from api.driver.views import driver_route
from api.schedule_type.views import schedule_type_route
from fastapi import FastAPI

from api.work_schedule_history.views import work_schedule_history_route


def setup_routes(app: FastAPI):
    """Настройка Роутов приложения."""
    app.include_router(driver_route)
    app.include_router(car_route)
    app.include_router(schedule_type_route)
    app.include_router(work_schedule_history_route)
