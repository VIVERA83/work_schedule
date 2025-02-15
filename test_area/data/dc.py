from dataclasses import dataclass
from datetime import datetime


@dataclass
class DriverFullData:
    driver: "Driver"
    work_schedule_history: "WorkScheduleHistory"
    schedule_type: "ScheduleType"
    car: "Car" = None


@dataclass
class ScheduleType:
    id: int
    name: str
    work_days: int
    weekend_days: int


@dataclass
class Driver:
    id: int
    name: str


@dataclass
class WorkScheduleHistory:
    id: int
    id_driver: int
    id_schedule_type: int
    date: datetime
    is_working: bool
    what_day: int


@dataclass
class Car:
    id: int
    car_number: str
    car_model: str
    name: str


@dataclass
class CarDriverAssign:
    id: int
    id_car: int
    id_driver: int


description__route = {
    "get_by_id": {
        "methods": ["GET"],
        "path": "/{id_}",
        "endpoint": None,
        "summary": "получить",
        "description": "Получить данные по id.",
        "params_annotation": {"id_": Annotated[int, ID]},
        "response_model": None,
    },
    "create": {
        "methods": ["POST"],
        "path": None,
        "endpoint": None,
        "summary": "создать",
        "description": "Создать машину.",
        "params_annotation": {"data": CarCreateSchema},
        "response_model": CarSchema,
    },
    "delete_by_id": {
        "methods": ["DELETE"],
        "path": "/{id_}",
        "endpoint": None,
        "summary": "получить",
        "description": "Получить данные по id.",
        "params_annotation": {"id_": Annotated[int, ID]},
        "response_model": None,
    },
    "update": {
        "methods": ["PUT"],
        "path": None,
        "endpoint": None,
        "summary": "создать",
        "description": "Создать машину.",
        "params_annotation": {"data": CarCreateSchema},
        "response_model": CarSchema,
    },
}
