class DBException(Exception):
    """
    Базовый класс для всех исключений, создаваемых этим модулем.
    """

    message = "Ошибка базы данных"

    def __init__(self, message: str = None):
        if message:
            self.message = message

    def __str__(self):
        return f"<{self.__class__.__name__}> : {self.message}"


class DBNotFoundException(DBException):
    """
    Исключение, которое выбрасывается, если в базе данных не найдена запись.
    """

    message = "Запись не найдена"
