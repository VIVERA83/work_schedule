"""Модуль запуска приложения."""

import uvicorn
from core.settings import UvicornSettings
from icecream import ic

ic.includeContext = True

if __name__ == "__main__":
    settings = UvicornSettings()
    uvicorn.run(
        app="core.setup:setup_app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        log_level=settings.log_level.swapcase(),
        reload=settings.reload,
    )
