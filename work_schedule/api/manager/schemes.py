from datetime import datetime

from pydantic import BaseModel, Field

from api.driver.schemes import DriverSchema
from api.work_schedule_history.schemes import WorkScheduleHistorySchema


class CreateSchema(BaseModel):
    name: str = Field(
        description="Производитель",
        examples=["MAN"],
        min_length=2,
        max_length=70,
    )
    id_schedule_type: int = Field(
        description="идентификатор типа расписания:",
        examples=["1"],
        gt=0
    )
    date: datetime = Field(
        description="дата начала графика, по умолчанию текущая дата",
        examples=[datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)],
        default=None,
    )
    is_working: bool = Field(
        description="флаг работы водителя",
        default=True,
    )
    what_day: int = Field(
        description="Который день, водитель работает(отдыхает).",
        default=1,
        gt=0,
    )


class FullDataDriverSchema(BaseModel):
    driver: DriverSchema
    work_schedule_history: WorkScheduleHistorySchema
