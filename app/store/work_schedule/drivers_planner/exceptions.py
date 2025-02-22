import re

from store.work_schedule.base.exceptions import ExceptionBase, pattern


class DataBaseConnectionException(ExceptionBase):
    args = ("Ошибка подключения к базе данных. Попробуйте позже.",)


class DataBaseUnknownException(ExceptionBase):
    args = ("Неизвестная ошибка базы данных.",)


class CarDriverAssociationDuplicateException(ExceptionBase):
    args = ("Указанная связь водителя и машины уже существует.",)
    code = 400


class  DriverScheduleNotFoundException(ExceptionBase):
    args = ("График работы не найден. Возможно в указанный период водителя не было",)
    code = 404

class ForeignKeyException(ExceptionBase):
    args = ("Не верная ссылка на таблицу типа расписания. id_schedule_type",)
    code = 400

    def __init__(self, *args, code: int = None, exception: Exception = None):
        super().__init__(*args, code=code, exception=exception)
        matches = re.findall(pattern, self.exception.args[0])
        self.args = (f"Нет записи с указанным {matches[1]}: {matches[2]}",)


class InternalDatabaseException(ExceptionBase):
    args = (
        "За машиной может быть закреплено не более 3 водителей. "
        "Превышено максимальное количество водителей, закрепленных за машиной."
        "Необходимо открепить водителя от машины.",
    )
    code = 400
