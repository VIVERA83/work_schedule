from datetime import datetime, timedelta

from work_schedule.store.scheduler.schedule_maker import ScheduleMaker

today_1 = datetime.now()
date_17_01_2020 = datetime(2020, 1, 17)
date_17_02_2020 = datetime(2020, 2, 17)
date_01_01_2020 = datetime(2020, 1, 1)
date_17_01_2021 = datetime(2021, 1, 17)

date_06_01_2025 = datetime(2025, 1, 6)
date_10_01_2025 = datetime(2025, 1, 10)
date_17_01_2025 = datetime(2025, 1, 17)
today_2 = datetime.now()

weekend_days_2 = 2

driver_0_id = 0
driver_0_name = "Иванов Иван Иванович"
driver_0_schedule_type_work_days = 4
driver_0_schedule_type_weekend_days = 2
driver_0_work_schedule_history_date = date_06_01_2025
driver_0_work_schedule_history_is_working = False
driver_0_work_schedule_history_what_day = 1

driver_1_id = 1
driver_1_name = "Сидоров Сидор Сидорович"
driver_1_work_schedule_history_date = date_06_01_2025
driver_1_schedule_type_work_days = 4
driver_1_schedule_type_weekend_days = 4
driver_1_work_schedule_history_is_working = True
driver_1_work_schedule_history_what_day = 4

is_working_true = True
what_day_1 = 1

driver_id_0 = 0

car_id_0 = 0
car_0_schedule_start_date = date_06_01_2025
car_0_name = "MAN TGM А124МК196"
car_1_name = "MAN TGS А777НН198"
days = 4
today = datetime.now()
other_date = today + timedelta(days=days)

car_0_schedule_make_result = {'06-01-2025': 'Р',
                              '07-01-2025': 'Р',
                              '08-01-2025': 'Р',
                              '09-01-2025': 'Р',
                              '10-01-2025': 'Р'}

driver_0_schedule_make_result = {'06-01-2025': 'В',
                                 '07-01-2025': 'В',
                                 '08-01-2025': 'Р',
                                 '09-01-2025': 'Р',
                                 '10-01-2025': 'Р'}

driver_1_schedule_make_result = {'06-01-2025': 'Р',
                                 '07-01-2025': 'В',
                                 '08-01-2025': 'В',
                                 '09-01-2025': 'В',
                                 '10-01-2025': 'В'}

merged_schedule = ['Р',
                   'Р',
                   'Иванов Иван Иванович',
                   'Иванов Иван Иванович',
                   'Иванов Иван Иванович']

schedule = ScheduleMaker(
    name=driver_0_name,
    schedule_start_date=date_17_01_2020,
    work_days=driver_0_schedule_type_work_days,
    weekend_days=weekend_days_2,
    is_working=is_working_true,
    what_day=what_day_1
)

car_0_s = ScheduleMaker(
    name=car_0_name,
    schedule_start_date=car_0_schedule_start_date,
    work_days=-1,
    weekend_days=-1,
    is_working=True,
    what_day=1,
)
car_1_s = ScheduleMaker(
    name=car_1_name,
    schedule_start_date=car_0_schedule_start_date,
    work_days=-1,
    weekend_days=-1,
    is_working=True,
    what_day=1,
)

driver_0_s = ScheduleMaker(
    name="driver_0_name",
    schedule_start_date=driver_0_work_schedule_history_date,
    work_days=driver_0_schedule_type_work_days,
    weekend_days=driver_0_schedule_type_weekend_days,
    is_working=driver_0_work_schedule_history_is_working,
    what_day=driver_0_work_schedule_history_what_day,
)
driver_1_s = ScheduleMaker(
    name="driver_1_name",
    schedule_start_date=driver_1_work_schedule_history_date,
    work_days=driver_1_schedule_type_work_days,
    weekend_days=driver_1_schedule_type_weekend_days,
    is_working=driver_1_work_schedule_history_is_working,
    what_day=driver_1_work_schedule_history_what_day,
)
# график такой же как у 0
driver_2_s = ScheduleMaker(
    name="driver_2_name",
    schedule_start_date=driver_0_work_schedule_history_date,
    work_days=driver_0_schedule_type_work_days,
    weekend_days=driver_0_schedule_type_weekend_days,
    is_working=driver_0_work_schedule_history_is_working,
    what_day=driver_0_work_schedule_history_what_day,
)
a = {'07-01-2025': 'B',
     '08-01-2025': 'P',
     '09-01-2025': 'P',
     '10-01-2025': 'P',
     '11-01-2025': 'P',
     '12-01-2025': 'B',
     '13-01-2025': 'B',
     '14-01-2025': 'P',
     '15-01-2025': 'P',
     '16-01-2025': 'P'}
