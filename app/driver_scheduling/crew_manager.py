from datetime import datetime
from typing import Union, Optional

from driver_scheduling.combined_employees_work_plan import CombinedEmployeesWorkPlan
from driver_scheduling.employee_work_plan import EmployeeWorkPlan
from driver_scheduling.schemas import (
    CrewSchema,
    CarSchema,
    DriverSchema,
    ScheduleHistorySchema,
)
from driver_scheduling.worker_schedule import Worker


class CrewsManager:
    def __init__(
        self, crews: dict[int, CrewSchema], start_date: datetime, end_date: datetime
    ):
        self.crews = crews
        self.start_date = start_date
        self.end_date = end_date
        self.combined_employees_work_plans = {}

    def __call__(self, *args, **kwargs):
        return self.get_combined_employees_work_plans()

    def get_combined_employees_work_plans(self):
        combined_employees_work_plans = {}
        for crew_id, crew in self.crews.items():
            car_workers = self.create_workers(crew.cars)
            driver_workers = self.create_workers(crew.drivers)
            employee_work_plans = self.create_employee_work_plans(
                car_workers, driver_workers
            )

            # Это проверка на то что машины и водителей в цикле не больше одного
            if employee_work_plans:
                combined_employees_work_plans[crew_id] = (
                    self.create_combined_employees_work_plan(employee_work_plans)
                )
        return combined_employees_work_plans

    @classmethod
    def create_combined_employees_work_plan(
        cls, employee_work_plans: list[EmployeeWorkPlan]
    ):
        return CombinedEmployeesWorkPlan(*employee_work_plans)

    def create_workers(self, workers_data: list[Union[CarSchema, DriverSchema]]):
        workers = []
        for worker in workers_data:
            if worker.schedules:
                if worker.schedules[0].schedule_start_date > self.start_date:
                    worker.schedules.insert(0, self.not_work_schedule_history_schema)
                workers.append(self.create_worker(worker.name, worker.schedules))
        return workers

    @staticmethod
    def create_employee_work_plans(
        car_workers: list[Worker], driver_workers: list[Worker]
    ):
        employee_work_plans = []
        for car_worker in car_workers:
            if car_worker is not None:
                employee_work_plans.append(
                    EmployeeWorkPlan(car_worker, *driver_workers)
                )
        return employee_work_plans

    @staticmethod
    def create_worker(
        name: str, schedules: list[ScheduleHistorySchema]
    ) -> Optional[Worker]:
        worker = None
        for schedule in schedules:
            if not worker:
                worker = Worker(
                    name=name,
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

    @property
    def not_work_schedule_history_schema(self) -> ScheduleHistorySchema:
        return ScheduleHistorySchema(
            schedule_start_date=self.start_date,
            work_days=-1,
            weekend_days=-1,
            is_working=True,
            what_day=0,
        )
