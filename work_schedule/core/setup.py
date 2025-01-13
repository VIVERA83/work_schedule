"""Модуль сборки приложения."""

from fastapi import FastAPI

from core.lifespan import lifespan
from core.logger import setup_logging
from core.middelware import setup_middleware
from core.routes import setup_routes
from core.settings import AppSettings


def setup_app() -> "FastAPI":
    """Создание и настройка основного FastAPI приложения.

    Returns:
        Application: Основное FastAPI приложение.
    """
    settings = AppSettings()
    app = FastAPI(
        lifespan=lifespan,
        version=settings.version,
        title=settings.title,
        description=settings.description,
    )
    app.logger = setup_logging()
    setup_middleware(app)
    setup_routes(app)
    app.logger.info(f"http://0.0.0.0:8008/docs/")
    return app
