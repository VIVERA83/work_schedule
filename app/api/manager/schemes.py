from datetime import datetime

from api.car.schemes import CarSchema
from api.driver.schemes import DriverSchema
from api.work_schedule_history.schemes import WorkScheduleHistorySchema
from pydantic import BaseModel, Field


class AddDriverSchema(BaseModel):
    name: str = Field(
        description="ФИО водителя",
        examples=["Филатов Александр Алексеевич"],
        min_length=2,
        max_length=70,
    )
    id_schedule_type: int = Field(
        description="идентификатор типа расписания:", examples=["1"], gt=0
    )
    date: datetime = Field(
        description="дата начала графика, по умолчанию текущая дата",
        examples=[
            datetime(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day,
            )
        ],
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


class AssignCarDriverSchema(BaseModel):
    driver_id: int
    car_id: int


class AssignCarDriverCreateSchema(AssignCarDriverSchema): ...


class AddCarSchema(BaseModel):
    name: str = Field(
        description="Производитель автомобиля",
        examples=["MAN"],
        min_length=2,
        max_length=70,
    )
    car_model: str = Field(
        description="Модель автомобиля", examples=["TGS"], min_length=2, max_length=70
    )
    car_number: str = Field(
        description="Номер автомобиля",
        examples=["о695рс196"],
        min_length=8,
        max_length=9,
    )
    id_schedule_type: int = Field(
        description="идентификатор типа расписания:", examples=["1"], gt=0
    )
    is_working: bool = Field(description="флаг работы автомобиля", default=True)
    what_day: int = Field(
        description="Который день, машина работает(отдыхает).", default=1, gt=0
    )
    date: datetime = Field(
        description="дата начала графика, по умолчанию текущая дата",
        examples=[
            datetime(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day,
            )
        ],
        default=None,
    )


class FullDataCarSchema(BaseModel):
    car: "CarSchema"
    work_schedule_history: "CarScheduleHistorySchema"


class CarScheduleHistorySchema(BaseModel):
    id_car: int = Field(description="идентификатор автомобиля", examples=["1"], gt=0)
    id_schedule_type: int = Field(
        description="идентификатор типа расписания:", examples=["1"], gt=0
    )
    date: datetime = Field(
        description="дата начала графика",
        default=datetime(
            year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
        ),
    )
    is_working: bool = Field(default=True, description="флаг работы водителя")
    what_day: int = Field(
        default=1, description="Который день, автомобиль работает.", gt=0
    )
