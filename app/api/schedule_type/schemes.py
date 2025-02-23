from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class ScheduleTypeCreateSchema(BaseModel):
    name: str = Field(
        description="Название типа расписания",
        examples=["4/2"],
        min_length=2,
        max_length=70,
    )
    work_days: int = Field(description="Количество рабочих дней", examples=["4"], gt=0)
    weekend_days: int = Field(
        description="Количество выходных дней", examples=["2"], gt=0
    )


class ScheduleTypeSchema(IdSchema, ScheduleTypeCreateSchema): ...


class ScheduleTypeUpdateSchema(ScheduleTypeSchema): ...
