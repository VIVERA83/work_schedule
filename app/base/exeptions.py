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
