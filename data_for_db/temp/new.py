import datetime

from icecream import ic

from driver_scheduling.crew_manager import CrewsManager
from driver_scheduling.schedule_manager import ScheduleManager
from driver_scheduling.schemas import CrewSchema, ScheduleHistorySchema, CarSchema, DriverSchema
from store.excel.dispatchplan import StatisticCalculator

data = {1: CrewSchema(id=1,
                      cars=[
                          CarSchema(id=1, name='MAN', model='TGL', number='О196МР196',
                                    schedules=[
                                        ScheduleHistorySchema(what_day=1, work_days=4, is_working=True, weekend_days=4,
                                                              schedule_start_date=datetime.datetime(2025, 1, 1, 0,
                                                                                                    0))]),
                          CarSchema(id=2, name='SITRAK', model='C7H', number='А012КС198', schedules=[
                              ScheduleHistorySchema(what_day=1, work_days=4, is_working=False, weekend_days=4,
                                                    schedule_start_date=datetime.datetime(2025, 1, 1, 0, 0))])],
                      drivers=[DriverSchema(id=3, name='Веселовский Александр Михайлович', schedules=[
                          ScheduleHistorySchema(what_day=1, work_days=4, is_working=False, weekend_days=2,
                                                schedule_start_date=datetime.datetime(2025, 1, 2, 0, 0))])]),



        # 2: CrewSchema(id=2, cars=[CarSchema(id=3, name='КАМАЗ', model='КОМПАС', number='О695РС198', schedules=[
        #     ScheduleHistorySchema(what_day=25, work_days=4, is_working=True, weekend_days=4,
        #                           schedule_start_date=datetime.datetime(2025, 1, 1, 0, 0))])],
        #               drivers=[DriverSchema(id=4, name='Агеев Сергей федорович', schedules=[])])
                       }

start_date = datetime.datetime(year=2025, month=1, day=10)
end_date = datetime.datetime(year=2025, month=1, day=15)
combined_employees_work_plans = CrewsManager(data, start_date, end_date)()
manager = ScheduleManager()
for combined_employees_work_plan in combined_employees_work_plans.values():
    ic(combined_employees_work_plan.get_schedule(start_date, end_date))
    ic(combined_employees_work_plan.employee_1.get_unused_employees(start_date, end_date))
    manager.add_combined_employees_work_plan(combined_employees_work_plan)

data = manager.get_schedule(start_date, end_date)
# ic(data)
# ic(StatisticCalculator(data))