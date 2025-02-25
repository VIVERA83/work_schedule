from datetime import datetime
from typing import Optional

from api.base.fields import ID_DRIVER, ID_SCHEDULE_TYPE, DATE_START, IS_WORKING, WHAT_DAY
from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class WorkScheduleHistoryCreateSchema(BaseModel):
    id_driver: int = ID_DRIVER
    id_schedule_type: int = ID_SCHEDULE_TYPE
    date: datetime = DATE_START
    is_working: bool = IS_WORKING
    what_day: int = WHAT_DAY


class WorkScheduleHistorySchema(IdSchema, WorkScheduleHistoryCreateSchema): ...


class WorkScheduleHistoryUpdateSchema(WorkScheduleHistorySchema):
    id_driver: Optional[int] = Field(default=None, description="идентификатор водителя", examples=["1"], gt=0)
    id_schedule_type: Optional[int] = Field(default=0, description="идентификатор типа расписания:", examples=["1"],
                                            gt=0)
    date: Optional[datetime] = Field(
        default=None,
        description="дата начала графика",
        examples=[datetime(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        )],
    )
    is_working: Optional[bool] = Field(default=None, description="флаг работы, рабочий или не рабочий день",
                                       examples=[True])
    what_day: Optional[int] = Field(default=None, description="Который день, машина работает(отдыхает).", gt=0,
                                    examples=[1])
