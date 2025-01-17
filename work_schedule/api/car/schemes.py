from pydantic import Field, BaseModel

from api.base.schemes import IdSchema


class CarCreateSchema(BaseModel):
    name: str = Field(
        description="Производитель",
        examples=["MAN"],
        min_length=2,
        max_length=70
    )
    car_number: str = Field(
        description="Номер автомобиля",
        examples=["о695рс196"],
    )
    car_type: str = Field(
        description="Модель автомобиля",
        examples=["TGS"],
        min_length=2
    )


class CarSchema(IdSchema, CarCreateSchema):
    ...
