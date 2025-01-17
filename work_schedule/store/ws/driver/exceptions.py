from store.ws.base.exceptions import ExceptionBase


class DriverNotFoundException(ExceptionBase):
    args = "Водитель не найден.",
    code = 404
