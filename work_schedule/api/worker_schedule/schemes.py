from datetime import datetime, timedelta
from typing import Annotated, Literal

from pydantic import BaseModel, Field


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
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day + 10
        ),
    )


WorkerScheduleSchema = Annotated[
    dict[str, Literal["P", "B"]],
    Field(
        description="данные для построения графика",
        examples=[{"20-01-2025": "P", "21-01-2025": "B"}],
    ),
]
