from datetime import datetime

from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class WorkScheduleHistoryCreateSchema(BaseModel):
    id_driver: int = Field(description="идентификатор водителя", examples=["1"], gt=0)
    id_schedule_type: int = Field(
        default="идентификатор типа расписания:", examples=["1"], gt=0
    )
    date: datetime = Field(
        default=datetime(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        ),
        description="дата начала графика",
    )
    is_working: bool = Field(default=True, description="флаг работы водителя")
    what_day: int = Field(
        default=1, description="Который день, водитель работает(отдыхает).", gt=0
    )


class WorkScheduleHistorySchema(IdSchema, WorkScheduleHistoryCreateSchema): ...


class WorkScheduleHistoryUpdateSchema(WorkScheduleHistorySchema): ...
