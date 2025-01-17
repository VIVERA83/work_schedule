from typing import TypeVar, Union

from sqlalchemy import UpdateBase, ValuesBase
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from sqlalchemy.sql import Select, Delete, Insert

Query = Union[ValuesBase, Select, UpdateBase, Delete, Insert]
Model = TypeVar("Model", bound=DeclarativeAttributeIntercept)
