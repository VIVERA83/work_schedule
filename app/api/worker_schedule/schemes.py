from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from fastapi import Query

from api.base.fields import DATE_START, DATE_END, WHAT_DAY, WORK_DAYS, IS_WORKING, WEEKEND_DAYS, CAR_MODEL, CAR_NUMBER, \
    CAR_NAME, DRIVER_NAME
from api.base.schemes import IdSchema

WorkerScheduleSchema = Annotated[
    dict[str, Literal["P", "B"]],
    Field(
        description="данные для построения графика",
        examples=[{"20-01-2025": "P", "21-01-2025": "B"}],
    ),
]

START_DATE = Query(
    description="дата начала графика построения графика",
    examples=["01-01-2025"],
    default=datetime(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
    ),
)

END_DATE = Query(
    description="дата начала графика построения графика",
    examples=["20-01-2025"],
    default=datetime(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
    ),
)


class WorkerScheduleCreateSchema(IdSchema):
    start_date: datetime = DATE_START
    end_date: datetime = DATE_END


class ScheduleHistorySchema(BaseModel):
    what_day: int = WHAT_DAY
    work_days: int = WORK_DAYS
    is_working: bool = IS_WORKING
    weekend_days: int = WEEKEND_DAYS
    schedule_start_date: datetime = DATE_START


class CarSchema(IdSchema):
    model: str = CAR_MODEL
    number: str = CAR_NUMBER
    schedules: list[ScheduleHistorySchema]
    name: str = CAR_NAME

    @field_validator("name", mode="before")
    def _(cls, value: str, values: ValidationInfo) -> str:
        """Вычисляемое поле: объединяет name model и number."""
        return f"{value} {values.data['model']} {values.data['number']}"


class DriverSchema(IdSchema):
    name: str = DRIVER_NAME
    schedules: list[ScheduleHistorySchema]


class CrewSchema(IdSchema):
    cars: list[CarSchema]
    drivers: list[DriverSchema]
