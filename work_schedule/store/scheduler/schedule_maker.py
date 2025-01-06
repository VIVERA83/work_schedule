from datetime import datetime

from work_schedule.store.scheduler.utils import get_timetable_period


class ScheduleMaker:
    def __init__(self,
                 name: str,
                 schedule_start_date: datetime,
                 work_days: int,
                 weekend_days: int,
                 is_working: bool,
                 what_day: int,
                 ):
        self.name = name
        self.schedule_start_date = schedule_start_date
        self.work_days = work_days
        self.weekend_days = weekend_days
        self.is_working = is_working
        self.what_day = what_day

    def make(self, start_date: datetime, end_date: datetime) -> dict[str, str]:
        self.validate_make_data(start_date, end_date)
        return self._make(start_date, end_date)

    def _make(self, start_date: datetime, end_date: datetime) -> dict[str, str]:
        return get_timetable_period(
            schedule_start_date=self.schedule_start_date,
            work_days=self.work_days,
            weekend_days=self.weekend_days,
            is_working=self.is_working,
            what_day=self.what_day,
            start_date=start_date,
            end_date=end_date,
        )

    def validate_make_data(self, start_date: datetime, end_date: datetime):
        start_date = datetime(year=start_date.year, month=start_date.month, day=start_date.day)
        end_date = datetime(year=end_date.year, month=end_date.month, day=end_date.day)
        err_msg = "\n"
        index = 0
        if start_date < self.schedule_start_date:
            index += 1
            err_msg += (
                f"{index}. Значение start_date должно быть больше или равно schedule_start_date.\n"
            )
        if end_date < self.schedule_start_date:
            index += 1
            err_msg += (
                f"{index}. Значение end_date должно быть больше или равно schedule_start_date\n"
            )
        if start_date > end_date:
            index += 1
            err_msg += (
                f"{index}. Значение start_date должно быть меньше или равно end_date.\n"
            )
        if err_msg != "\n":
            raise ValueError(err_msg)
