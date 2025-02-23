from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo
from fastapi import Query


class WorkerScheduleCreateSchema(BaseModel):
    id_: int = Field(description="идентификатор объекта", examples=["1"])
    start_date: datetime = Field(
        description="дата начала графика построения графика",
        default=datetime(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        ),
    )
    end_date: datetime = Field(
        description="дата окончания построения графика",
        default=datetime(
            year=datetime.now().year,
            month=datetime.now().month,
            # может выпадать ошибка, из-за того сложение дней которые выходят за рамки месяца
            day=datetime.now().day,
        ),
    )


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
    ))

END_DATE = Query(
    description="дата начала графика построения графика",
    examples=["20-01-2025"],
    default=datetime(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
    ))


class ScheduleHistorySchema(BaseModel):
    what_day: int = Field()
    work_days: int = Field()
    is_working: bool = Field()
    weekend_days: int = Field()
    schedule_start_date: datetime = Field()


class CarSchema(BaseModel):
    id: int = Field()
    model: str = Field()
    number: str = Field()
    schedules: list[ScheduleHistorySchema] = Field()
    name: str = Field()

    @field_validator("name", mode="before")
    def _(cls, value: str, values: ValidationInfo) -> str:
        """Вычисляемое поле: объединяет name model и number."""
        return f"{value} {values.data['model']} {values.data['number']}"


class DriverSchema(BaseModel):
    id: int = Field()
    name: str = Field()
    schedules: list[ScheduleHistorySchema] = Field()


class CrewSchema(BaseModel):
    id: int = Field()
    cars: list[CarSchema] = Field()
    drivers: list[DriverSchema] = Field()
