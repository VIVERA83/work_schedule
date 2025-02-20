from typing import Optional

from api.worker_schedule.schemes import ScheduleHistorySchema
from store.scheduler.worker_schedule import Worker


def create_worker(name: str, schedules: list[ScheduleHistorySchema]) -> Optional[Worker]:
    worker = None
    for schedule in schedules:
        if not worker:
            worker = Worker(name=name,
                            schedule_start_date=schedule.schedule_start_date,
                            work_days=schedule.work_days,
                            weekend_days=schedule.weekend_days,
                            is_working=schedule.is_working,
                            what_day=schedule.what_day,
                            )
        else:
            worker.add_worker_schedule(
                schedule_start_date=schedule.schedule_start_date,
                work_days=schedule.work_days,
                weekend_days=schedule.weekend_days,
                is_working=schedule.is_working,
                what_day=schedule.what_day,

            )
    return worker

