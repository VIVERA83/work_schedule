import uuid
from datetime import datetime
from pathlib import Path

from core.settings import TempFolderSettings


def create_file_name(start_date: datetime, end_date: datetime) -> str:
    """Создает имя файла для экспорта.

    :param start_date: Начало диапазона
    :param end_date: Конец диапазона
    :return: Абсолютный путь к файлу в виде строки
    """

    temp_dir = Path(TempFolderSettings().temp_dir)
    unique_id = uuid.uuid4().hex[:8]
    file_name = f"{start_date.strftime('%Y-%m-%d')}-{end_date.strftime('%Y-%m-%d')}_{unique_id}.xlsx"
    file_path = temp_dir / file_name
    return str(file_path.absolute())
