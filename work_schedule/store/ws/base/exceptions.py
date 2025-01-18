from functools import wraps
from typing import Type

from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError, NoResultFound


class ExceptionBase(Exception):
    """Базовый класс для всех исключений."""

    args = ("Неизвестное исключение.",)
    exception = None
    code = 500

    def __init__(self, *args, code: int = None, exception: Exception = None):

        if args:
            self.args = args
        if exception:
            self.exception = exception
        if code:
            self.code = code

    def __str__(self):
        return f"Исключение: {self.args[0]}, код: {self.code}"


class DataBaseConnectionException(ExceptionBase):
    args = ("Ошибка подключения к базе данных. Попробуйте позже.",)


class DataBaseUnknownException(ExceptionBase):
    args = ("Неизвестная ошибка базы данных.",)


class DuplicateException(ExceptionBase):
    args = ("Повторяющие значение в таблице. Придумайте другое значение.",)
    code = 400


class NotFoundException(ExceptionBase):
    args = ("Запись не найдена.",)
    code = 404


class ForeignKeyException(ExceptionBase):
    args = ("Не верно указана связь с таблицей.",)
    code = 400
