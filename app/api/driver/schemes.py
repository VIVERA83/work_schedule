from api.base.fields import DRIVER_NAME
from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class DriverCreateSchema(BaseModel):
    name: str = DRIVER_NAME


class DriverSchema(IdSchema, DriverCreateSchema): ...


class DriverUpdateSchema(DriverSchema): ...
