import sys

from core.settings import LogSettings
from loguru import logger


def setup_logging() -> logger:
    """Настройка логирования в приложении.

    Подробнее о Loguru можно почитать в документации.
    https://github.com/Delgan/loguru
    """
    settings = LogSettings()
    logger.configure(
        **{
            "handlers": [
                {
                    "sink": sys.stderr,
                    "level": settings.level,
                    "backtrace": settings.traceback,
                },
            ],
        }
    )
    return logger
