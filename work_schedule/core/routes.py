from api.car.views import car_route
from api.driver.views import driver_route
from api.schedule_type.views import schedule_type_route
from fastapi import FastAPI


def setup_routes(app: FastAPI):
    """Настройка Роутов приложения."""
    app.include_router(driver_route)
    app.include_router(car_route)
    app.include_router(schedule_type_route)
