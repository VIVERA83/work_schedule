import os
from typing import Literal

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))

LOG_LEVEL = Literal[
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARN",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]


class Base(BaseSettings):
    class Config:
        env_nested_delimiter = "__"
        env_file = os.path.join(BASE_DIR, ".env")
        enf_file_encoding = "utf-8"
        extra = "ignore"


class LogSettings(Base):
    level: LOG_LEVEL = "INFO"
    traceback: bool = True


class PostgresSettings(Base):
    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: str
    postgres_schema: str

    def dsn(self, show_secret: bool = False) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=self.postgres_user,
            password=(
                self.postgres_password.get_secret_value()
                if show_secret
                else self.postgres_password
            ),
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db,
        )


class UvicornSettings(Base):
    host: str
    port: int
    workers: int
    log_level: LOG_LEVEL = "INFO"
    reload: bool = True


class AppSettings(Base):
    title: str = "График работы персонала"
    description: str = "API документация по работе с графиком персонала."
    version: str = "0.0.1"


class TempFolderSettings(Base):
    temp_dir: str = os.path.join(BASE_DIR, "app/temp")

    @field_validator("temp_dir", mode="before")
    def _(cls, v: str) -> str:  # noqa:
        """Проверка наличия папки для временных файлов"""

        temp_dir = os.path.join(BASE_DIR, "app/temp", v)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        return os.path.join(BASE_DIR, "app/temp", v)
