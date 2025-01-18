from functools import wraps
from typing import Type

from asyncpg import UniqueViolationError
from icecream import ic
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


def exception_handler(
    not_found: Type[ExceptionBase] = NotFoundException,
    duplicate: Type[ExceptionBase] = DuplicateException,
    foreign_key: Type[ExceptionBase] = ForeignKeyException,
):
    def inner(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except (IntegrityError, NoResultFound, UniqueViolationError) as e:
                self.logger.warning(str(e))
                if "duplicate key value violates unique constraint" in str(e):
                    raise duplicate(exception=e)
                if "violates foreign key constraint" in str(e):
                    raise foreign_key(exception=e)
                raise not_found(exception=e)
            except IOError as e:
                self.logger.error(str(e))
                if e.errno == 111:
                    raise DataBaseConnectionException(exception=e)
                raise DataBaseUnknownException(exception=e)
            except Exception as e:
                self.logger.error(str(e))
                raise DataBaseUnknownException(exception=e)

        return wrapper

    return inner
