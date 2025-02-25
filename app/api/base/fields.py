# Общие типы полей для многих схем, которые используются в нескольких схем
from datetime import datetime

from pydantic import Field

DRIVER_NAME = Field(
    description="Фамилия Имя Отчество",
    examples=["Иванов Иван Иванович"],
    min_length=2,
    max_length=70,
)

CAR_NAME = Field(
    description="Производитель",
    examples=["MAN"],
    min_length=2,
    max_length=70,
)

CAR_MODEL = Field(
    description="Модель автомобиля", examples=["TGS"], min_length=2
)
CAR_NUMBER = Field(
    description="Номер автомобиля",
    examples=["о695рс196"],
)

ID_DRIVER = Field(description="идентификатор водителя", examples=["1"], gt=0)
ID_CAR = Field(description="идентификатор машины", examples=["1"], gt=0)
ID_CREW = Field(description="идентификатор экипажа", examples=["1"], gt=0)
ID_SCHEDULE_TYPE = Field(description="идентификатор типа расписания:", examples=["1"], gt=0)

WORK_DAYS = Field(description="Количество рабочих дней", examples=["4"], gt=0)
IS_WORKING = Field(description="флаг работы, рабочий или не рабочий день", examples=[True])
WEEKEND_DAYS = Field(description="Количество не рабочих дней", examples=["2"], gt=0)
WHAT_DAY = Field(description="Который день, машина работает(отдыхает).", gt=0, examples=[1])

DATE_START = Field(
    description="дата начала графика",
    examples=[datetime(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
    )],
)
DATE_END = Field(
    description="дата окончания графика",
    examples=[datetime(
        year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
    )],
)