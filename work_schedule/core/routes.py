from fastapi import FastAPI

from api.driver.views import driver_route


def setup_routes(app: FastAPI):
    """Настройка Роутов приложения."""
    app.include_router(driver_route)
    # app.include_router(category_route)
    # app.include_router(product_route)
