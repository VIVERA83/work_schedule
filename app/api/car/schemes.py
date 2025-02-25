from typing import Optional

from api.base.fields import CAR_NAME, CAR_MODEL, CAR_NUMBER
from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class CarCreateSchema(BaseModel):
    name: str = CAR_NAME
    car_model: str = CAR_MODEL
    car_number: str = CAR_NUMBER


class CarSchema(IdSchema, CarCreateSchema): ...


class CarUpdateSchema(IdSchema):
    name: Optional[str] = Field(
        default=None,
        description="Производитель",
        examples=["MAN"],
        min_length=2,
        max_length=70,
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
