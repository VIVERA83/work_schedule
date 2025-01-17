from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import ForeignKey, DATETIME, func, Index, CheckConstraint, Table, Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP

from store.db.postgres.base import Base, BaseModel

car_driver_association_table = Table(
    'car_driver_association', Base.metadata,
    Column('car_id', Integer, ForeignKey('car.id')),
    Column('driver_id', Integer, ForeignKey('driver.id'))
)


@dataclass
class CarModel(Base, BaseModel):
    __tablename__ = "car"

    name: Mapped[str] = mapped_column(unique=True)
    car_model: Mapped[str] = mapped_column(unique=True)
    car_number: Mapped[str] = mapped_column(unique=True)

    # drivers = relationship("DriverModel",
    #                        secondary=car_driver_association_table,
    #                        back_populates="cars",
    #                        )


@dataclass
class DriverModel(Base, BaseModel):
    __tablename__ = "driver"

    name: Mapped[str] = mapped_column()
    # cars = relationship("CarModel",
    #                     secondary=car_driver_association_table,
    #                     back_populates="drivers",
    #                     )


@dataclass
class ScheduleTypeModel(Base, BaseModel):
    __tablename__ = "schedule_types"

    __table_args__ = (
        Index('type_index', "name", "work_days", "weekend_days"),
    )

    name: Mapped[str] = mapped_column()
    work_days: Mapped[int] = mapped_column(CheckConstraint("work_days >= 1"))
    weekend_days: Mapped[int] = mapped_column(CheckConstraint("weekend_days >= 1"))


@dataclass
class WorkScheduleHistoryModel(Base, BaseModel):
    __tablename__ = "work_schedule_history"

    id_driver: Mapped[int] = mapped_column(ForeignKey("driver.id", ondelete="CASCADE"), nullable=True)
    id_schedule_type: Mapped[int] = mapped_column(ForeignKey("schedule_types.id", ondelete="CASCADE"), nullable=True)

    date: Mapped[DATETIME] = mapped_column(TIMESTAMP, default=datetime.now(), server_default=func.current_timestamp())
    is_working: Mapped[bool] = mapped_column(default=True)
    what_day: Mapped[int] = mapped_column(default=1)

    # driver: Mapped[Optional["DriverModel"]] = relationship("DriverModel", cascade="delete")
