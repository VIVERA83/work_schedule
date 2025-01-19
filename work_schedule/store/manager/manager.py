from datetime import datetime
from typing import TYPE_CHECKING

from icecream import ic
from store.scheduler.worker_schedule import WorkerSchedule

if TYPE_CHECKING:
    from store.store import Store


class ManagerWorkerSchedule:
    def __init__(self, store: "Store"):
        self.store = store

    async def get_worker_schedule(
        self, id_: int, start_date: datetime, end_date: datetime
    ):
        """Получение расписания водителя."""
        result = await self.store.manager.get_current_worker_schedule_by_id(id_)
        ic(result)
        schedule = WorkerSchedule(**result).make_schedule(start_date, end_date)
        return schedule
