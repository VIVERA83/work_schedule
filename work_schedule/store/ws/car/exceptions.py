from store.ws.base.exceptions import ExceptionBase


class CarDuplicateException(ExceptionBase):
    args = ("Машина с указанным номером, уже существует.",)
    code = 400
