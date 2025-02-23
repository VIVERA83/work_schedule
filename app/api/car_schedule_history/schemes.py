from datetime import datetime

from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class CarScheduleHistoryCreateSchema(BaseModel):
    id_car: int = Field(description="идентификатор машины", examples=["1"], gt=0)
    id_schedule_type: int = Field(
        default="идентификатор типа расписания:", examples=["1"], gt=0
    )
    date: datetime = Field(
        default=datetime(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        ),
        description="дата начала графика",
    )
    is_working: bool = Field(default=True, description="флаг работы машины")
    what_day: int = Field(
        default=1, description="Который день, машина работает(отдыхает).", gt=0
    )


class CarScheduleHistorySchema(IdSchema, CarScheduleHistoryCreateSchema): ...


class CarScheduleHistoryUpdateSchema(CarScheduleHistorySchema): ...
