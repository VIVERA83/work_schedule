"""Модуль сборки приложения."""

from core.lifespan import lifespan
from core.logger import setup_logging
from core.middelware import setup_middleware
from core.routes import setup_routes
from core.settings import AppSettings
from fastapi import FastAPI


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
    setup_routes(app, logger=app.logger)
    app.logger.info(f"http://0.0.0.0:8008/docs/")
    return app
