from datetime import datetime
from typing import Optional

from api.base.fields import ID_CAR, ID_SCHEDULE_TYPE, DATE_START, IS_WORKING, WHAT_DAY
from api.base.schemes import IdSchema
from pydantic import BaseModel, Field


class CarScheduleHistoryCreateSchema(BaseModel):
    id_car: int = ID_CAR
    id_schedule_type: int = ID_SCHEDULE_TYPE
    date: datetime = DATE_START
    is_working: bool = IS_WORKING
    what_day: int = WHAT_DAY


class CarScheduleHistorySchema(IdSchema, CarScheduleHistoryCreateSchema): ...


class CarScheduleHistoryUpdateSchema(IdSchema):
    id_car: Optional[int] = Field(default=None, description="идентификатор машины", examples=["1"], gt=0)
    id_schedule_type: Optional[int] = Field(default=None, description="идентификатор типа расписания:", examples=["1"],
                                            gt=0)
    date: Optional[datetime] = Field(
        default=None,
        description="дата начала графика",
        examples=[datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)],

    )
    is_working: Optional[bool] = Field(default=None, description="флаг работы, рабочий или не рабочий день",
                                       examples=[True])
    what_day: Optional[int] = Field(description="Который день, машина работает(отдыхает).", gt=0, examples=[1]
                                    )
