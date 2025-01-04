from dataclasses import dataclass
from datetime import datetime


@dataclass
class DriverFullData:
    driver: "Driver"
    work_schedule_history: "WorkScheduleHistory"
    schedule_type: "ScheduleType"

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
