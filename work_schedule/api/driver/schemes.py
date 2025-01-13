from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from api.base.schemes import IdSchema

id_: int = Field(
    description="уникальный идентификатор объекта",
    examples=["1"]
)
name: str = Field(description="Фамилия Имя Отчество",
                  examples=["Иванов Иван Иванович"],
                  min_length=5,
                  max_length=70
                  )

schedule_type_id: int = Field(
    description="идентификатор типа расписания",
    examples=[1],
    gt=0
)
is_working: bool = Field(
    default=True,
    description="флаг работы водителя"
)
what_day: int = Field(
    default=1,
    description="Который день, водитель работает(отдыхает)."
)


class DriverFullDataSchema(BaseModel):
    driver: "DriverSchema"
    work_schedule_history: "WorkScheduleHistorySchema"
    schedule_type: "ScheduleTypeSchema"
    car: Optional["CarSchema"] = None


class DriverCreateSchema(BaseModel):
    name: str = name
    schedule_type_id: int = schedule_type_id
    is_working: bool = is_working
    what_day: int = what_day


class DriverSchema(IdSchema):
    name: str = name


class WorkScheduleHistorySchema(IdSchema):
    id_driver: int = id_
    id_schedule_type: int = schedule_type_id
    date: datetime = Field(default_factory=datetime.now)
    is_working: bool = is_working
    what_day: int = what_day


class ScheduleTypeSchema(IdSchema):
    name: str = Field(description="Название типа расписания",
                      examples=["4/2"],
                      min_length=3,
                      max_length=70
                      )
    works_days: int = Field(
        description="Количество дней работы водителя, в графике",
        default=4,
        examples=[4],
        gt=0,
    )
    weekend_days: int = Field(
        description="Количество дней выходных в графике",
        default=2,
        examples=[2],
        gt=0,
    )


# TODO  нужна проверка то что все буквы русские
class CarSchema(IdSchema):
    car_number: str = Field(
        description="Номер автомобиля",
        examples=["о695рс196"],
    )
    car_model: str = Field(
        description="Модель автомобиля",
        examples=["TGS"],
        min_length=2,
    )
    name: str = Field(
        description="Название производителя автомобиля",
        examples=["MAN"],
    )
