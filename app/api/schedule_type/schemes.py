from typing import Optional

from api.base.fields import WORK_DAYS, WEEKEND_DAYS
from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class ScheduleTypeCreateSchema(BaseModel):
    name: str = Field(
        description="Название типа расписания",
        examples=["4/2"],
        min_length=2,
        max_length=70,
    )
    work_days: int = WORK_DAYS
    weekend_days: int = WEEKEND_DAYS


class ScheduleTypeSchema(IdSchema, ScheduleTypeCreateSchema): ...


class ScheduleTypeUpdateSchema(IdSchema):
    name: Optional[str] = Field(
        default=None,
        description="Название типа расписания",
        examples=["4/2"],
        min_length=2,
        max_length=70,
    )
    work_days: Optional[int] = Field(default=None, description="Количество рабочих дней", examples=["4"], gt=0)
    weekend_days: Optional[int] = Field(default=None, description="Количество не рабочих дней", examples=["2"], gt=0)
