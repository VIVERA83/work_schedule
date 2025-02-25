from typing import Optional

from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class CarCreateSchema(BaseModel):
    name: str = Field(

        description="Производитель", examples=["MAN"], min_length=2, max_length=70
    )
    car_model: str = Field(
        description="Модель автомобиля", examples=["TGS"], min_length=2
    )
    car_number: str = Field(
        description="Номер автомобиля",
        examples=["о695рс196"],
    )


class CarSchema(IdSchema, CarCreateSchema): ...


class CarUpdateSchema(IdSchema):
    name: Optional[str] = Field(
        default=None,
        description="Производитель", examples=["MAN"], min_length=2, max_length=70
    )
    car_model: Optional[str] = Field(
        default=None,
        description="Модель автомобиля", examples=["TGS"], min_length=2
    )
    car_number: Optional[str] = Field(
        default=None,
        description="Номер автомобиля",
        examples=["о695рс196"],
    )
