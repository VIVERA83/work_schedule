from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class DriverCreateSchema(BaseModel):
    name: str = Field(
        description="Фамилия Имя Отчество",
        examples=["Иванов Иван Иванович"],
        min_length=2,
        max_length=70,
    )


class DriverSchema(IdSchema, DriverCreateSchema): ...


class DriverUpdateSchema(DriverSchema): ...
