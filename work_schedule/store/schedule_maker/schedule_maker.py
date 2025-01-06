from datetime import datetime

from work_schedule.store.schedule_maker.utils import get_timetable_period, is_working_day, dates_comparison


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

    def is_working_day(self, date: datetime) -> bool:
        return is_working_day(
            schedule_start_date=self.schedule_start_date,
            work_days=self.work_days,
            weekend_days=self.weekend_days,
            date=date,
            is_working=self.is_working,
            what_day=self.what_day,
        )[0]

    def validate_make_data(self, start_date: datetime, end_date: datetime):
        err_msg = "\n"
        index = 0
        if not dates_comparison(start_date, self.schedule_start_date):
            index += 1
            err_msg += (
                f"{index}. Значение start_date должно быть больше schedule_start_date.\n"
            )
        if not dates_comparison(end_date, self.schedule_start_date):
            index += 1
            err_msg += (
                f"{index}. Значение end_date должно быть больше schedule_start_date\n"
            )
        if dates_comparison(start_date, end_date):
            index += 1
            err_msg += (
                f"{index}. Значение start_date должно быть меньше end_date.\n"
            )
        if err_msg != "\n":
            raise ValueError(err_msg)
