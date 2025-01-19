from datetime import datetime

from pydantic import BaseModel, Field


class CreateSchema(BaseModel):
    name: str = Field(
        description="Производитель", examples=["MAN"], min_length=2, max_length=70
    )
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
