from datetime import datetime

from work_schedule.store.scheduler.schedule_maker import WorkerSchedule


class WorkScheduleDriver:
    def __init__(self,
                 driver_schedules: dict[int, WorkerSchedule],
                 car_schedules: dict[int, WorkerSchedule],
                 relationships: dict[int, list[int]],  # car, driver
                 ) -> None:
        self.driver_schedules = driver_schedules
        self.car_schedules = car_schedules
        self.relationships = relationships

    def create(self, start_date: datetime, end_date: datetime, ):
        time_table = {}
        car_buffer = []
        for car_id, car_maker in self.car_schedules.items():
            if driver_ids:=self.relationships.get(car_id, None):
                driver_time_tables = []
                for driver_id in driver_ids:
                    print(driver_id)



            else:
                car_buffer.append(car_id)


