import os
from logging import Logger


def delete_file(path_to_file: str, logger: Logger) -> None:
    """Удаление файла."""

    if os.path.exists(path_to_file):
        os.remove(path_to_file)
        logger.info(f"Временный файл {path_to_file} удален")
    else:
        logger.warning(f"Временный файл {path_to_file} не найден")
