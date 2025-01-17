from dataclasses import dataclass
from typing import Optional, Union
from logging import Logger

from sqlalchemy import text

from store.ws.models import DriverModel
from work_schedule.store.db.data.exceptions import DBNotFoundException

ANY_TYPE = Union[str, int, float, bool, list, dict]


class BaseDB:
    class Meta:
        db = None
        dataclass = None

    def __init__(self):
        self.__db: Optional["PostgresAccessor"] = None
        if self.Meta.db is None:
            raise DBNotFoundException()
        else:
            self.__db = self.Meta.db
        self.logger = Logger(__name__)
        self.logger.info(f"{self.__class__.__name__} инициализирован.")

    @property
    def db(self):
        return self.__db

    async def get_by_id(self, brand_id: int):
        smtp = text(f"""SELECT * FROM brands WHERE id = {brand_id}""")
        print(type(smtp))
        result = await self.db.query_execute(smtp)
        print(1,result)
        return DriverModel(**result.mappings().one())

    # def get_by_id(self, id_: int) -> Union[dict, dataclass]:
    #     """Вывод данных по id.
    #
    #     Id это порядковый номер записи в списке, порядковый номер записи равен id внутри элемента списка.
    #     """
    #     result = None
    #     try:
    #         result = self.db[id_]
    #         return self.Meta.dataclass(**result)
    #     except IndexError:
    #         raise DBNotFoundException(f"<{self.__class__.__name__}> : Запись с id {id_} не найдена")
    #     except AttributeError:
    #         return result

    def get_by_filter(self, field_name: str, field_value: ANY_TYPE = None) -> list[dict]:
        """Вывод данных по значению поля.
        """
        result = []
        for item in self.db:
            value = item.get(field_name, None)
            if (not value is None) and (value == field_value):
                result.append(item)
        return result

    def create(self, data: dict) -> Union[dict, dataclass]:
        """Создание записи."""
        data["id"] = len(self.db)
        self.db.append(data)
        try:
            return self.Meta.dataclass(**data)
        except AttributeError:
            return data
