from dataclasses import dataclass
from typing import Optional, Union

from work_schedule.store.db.data.exceptions import DBNotFoundException

ANY_TYPE = Union[str, int, float, bool, list, dict]


class BaseDB:
    class Meta:
        db = None
        dataclass = None

    def __init__(self):
        self.__db: Optional[list[dict]] = None
        if self.Meta.db is None:
            self.__db = [{}]
        else:
            self.__db = self.Meta.db

    @property
    def db(self):
        return self.__db

    def get_by_id(self, id_: int) -> Union[dict, dataclass]:
        """Вывод данных по id.

        Id это порядковый номер записи в списке, порядковый номер записи равен id внутри элемента списка.
        """
        result = None
        try:
            result = self.db[id_]
            return self.Meta.dataclass(**result)
        except IndexError:
            raise DBNotFoundException
        except AttributeError:
            return result

    def get_by_filter(self, field_name: str, field_value: ANY_TYPE = None) -> list[dict]:
        """Вывод данных по значению поля.
        """
        result = []
        for item in self.db:
            value = item.get(field_name, None)
            if (not value is None) and (value == field_value):
                result.append(item)
        return result
