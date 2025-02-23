from store.work_schedule.base.exceptions import ExceptionBase


class CarDuplicateException(ExceptionBase):
    args = ("Машина с указанным номером, уже существует.",)
    code = 400
