from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from store.db.postgres.base import Base, BaseModel


@dataclass
class CarDriverAssociationModel(Base, BaseModel):
    __tablename__ = "car_driver_association"

    __table_args__ = (
        Index("car_driver_association_index", "car_id", "driver_id", unique=True),
    )

    car_id: Mapped[int] = mapped_column(ForeignKey("car.id", ondelete="CASCADE"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("driver.id", ondelete="CASCADE"))


@dataclass
class CarModel(Base, BaseModel):
    __tablename__ = "car"

    name: Mapped[str] = mapped_column()
    car_model: Mapped[str] = mapped_column()
    car_number: Mapped[str] = mapped_column(unique=True)


@dataclass
class DriverModel(Base, BaseModel):
    __tablename__ = "driver"

    name: Mapped[str] = mapped_column()


@dataclass
class ScheduleTypeModel(Base, BaseModel):
    __tablename__ = "schedule_types"

    __table_args__ = (
        Index("type_index", "name", "work_days", "weekend_days", unique=True),
    )

    name: Mapped[str] = mapped_column()
    work_days: Mapped[int] = mapped_column(CheckConstraint("work_days >= 1"))
    weekend_days: Mapped[int] = mapped_column(CheckConstraint("weekend_days >= 1"))


@dataclass
class WorkScheduleHistoryModel(Base, BaseModel):
    __tablename__ = "work_schedule_history"

    id_driver: Mapped[int] = mapped_column(
        ForeignKey("driver.id", ondelete="CASCADE"), nullable=True
    )
    id_schedule_type: Mapped[int] = mapped_column(
        ForeignKey("schedule_types.id", ondelete="CASCADE"), nullable=True
    )

    date: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=True
    )
    is_working: Mapped[bool] = mapped_column(default=True)
    what_day: Mapped[int] = mapped_column(default=1)
