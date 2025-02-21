from datetime import datetime

from pydantic import BaseModel, Field


class ScheduleHistorySchema(BaseModel):
    what_day: int = Field()
    work_days: int = Field()
    is_working: bool = Field()
    weekend_days: int = Field()
    schedule_start_date: datetime = Field()


class CarSchema(BaseModel):
    id: int = Field()
    name: str = Field()
    model: str = Field()
    number: str = Field()
    schedules: list[ScheduleHistorySchema] = Field()


class DriverSchema(BaseModel):
    id: int = Field()
    name: str = Field()
    schedules: list[ScheduleHistorySchema] = Field()


class CrewSchema(BaseModel):
    id: int = Field()
    cars: list[CarSchema] = Field()
    drivers: list[DriverSchema] = Field()
