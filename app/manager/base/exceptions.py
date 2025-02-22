from functools import wraps

from base.exeptions import ExceptionBase


class UnknownException(ExceptionBase):
    args = ("Неизвестная ошибка. Попробуйте позже.",)


class IncorrectInputDataException(ExceptionBase):
    args = ("Некорректные входные данные.",)


def exception_handler(method_name: str = ""):
    def inner(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except ValueError as e:
                self.logger.error(
                    f"{self.__class__.__name__}.{method_name}:\n{args=}\n{kwargs=}\nerror={e}"
                )
                raise IncorrectInputDataException(
                    e.args,
                    exception=e,
                    code=400,
                )
            except Exception as e:
                self.logger.error(
                    f"{self.__class__.__name__}.{method_name}:\n{args=}\n{kwargs=}\nerror={e}"
                )
                raise UnknownException(exception=e)

        return wrapper

    return inner
