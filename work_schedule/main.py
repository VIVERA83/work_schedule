# from icecream import ic
# from datetime import datetime, timedelta
#
# from work_schedule.store.db.data.exceptions import DBNotFoundException
# from work_schedule.store.db.db import DB
#
# from work_schedule.store.scheduler.schedule_maker import ScheduleMaker
# from work_schedule.store.scheduler.utils import timetable_work, is_working_day, get_timetable_period
#
# ic.includeContext = True
#
#
# # date_string = datetime.now().strftime("%Y-%m-%d")
# # date_format = '%Y-%m-%d'
# #
# # date_object = datetime.strptime(date_string, date_format)
#
#
# def test_schiduler():
#     db = DB()
#     new_driver = {"name": "Федоров Александр Константинович"}
#     days = 4
#     # добавили нового водителя
#     driver = db.creat_driver("Федоров Александр Константинович",
#                              1,
#                              False,
#                              4,
#                              )
#     # создали расписание на водителя
#     timetable = timetable_work(
#         end=datetime.now() + timedelta(days=days),
#         work_days=driver.schedule_type.work_days,
#         weekend_days=driver.schedule_type.weekend_days,
#     )
#     # проверка на рабочий день
#     is_working = is_working_day(
#         schedule_start_date=datetime.now(),
#         work_days=driver.schedule_type.work_days,
#         weekend_days=driver.schedule_type.weekend_days,
#         date=datetime.now() + timedelta(days=days - 4),
#     )
#     control_date = (datetime.now() + timedelta(days=days - 4)).date().strftime("%d-%m-%Y")
#     data = timetable.get(control_date)
#     assert is_working[0] == False if data == "В" else True
#
#
# def drivers(db: DB):
#     index = 0
#     while True:
#         try:
#             yield db.get_full_data_driver_by_id(index)
#             index += 1
#         except DBNotFoundException:
#             print("Всего водителей: ", index)
#             break
#
# def cars(db: DB):
#     index = 0
#     while True:
#         try:
#             yield db.get_car_by_id(index)
#             index += 1
#         except DBNotFoundException:
#             print("Всего машин: ", index)
#             break
#
# if __name__ == "__main__":
#     test_schiduler()
#     db = DB()
#
#     days = 4
#     today = datetime.now()
#     other_date = datetime.now() + timedelta(days=days)
#
#     driver_1 = next(drivers(db))
#     driver_s = ScheduleMaker(
#         name=driver_1.driver.name,
#         schedule_start_date=driver_1.work_schedule_history.date,
#         work_days=driver_1.schedule_type.work_days,
#         weekend_days=driver_1.schedule_type.weekend_days,
#         is_working=driver_1.work_schedule_history.is_working,
#         what_day=driver_1.work_schedule_history.what_day,
#     )
#     car_1 = next(cars(db))
#     car_1_s = ScheduleMaker(
#         name=f"{car_1.car_model} {car_1.car_number}",
#         schedule_start_date=driver_1.work_schedule_history.date,
#         work_days=-1,
#         weekend_days=-1,
#         is_working=True,
#         what_day=1,
#     )
#     ic(car_1_s.make_schedule(today, other_date))
#
#     # ic(today.date().today(), other_date.date(), driver_s.schedule_start_date.date())
#     r = driver_s.make_schedule(today, other_date)
#     ic(r)
#     # ic(driver_1)
#
# # def get_timetable(schedule_start_date: datetime,
# #                   work_days: int,
# #                   weekend_days: int,
# #                   is_working: bool,
# #                   what_day: int,
# #                   start_date: datetime,
# #                   end_date: datetime
# #                   ):
# #     # находим заданию дату работает или нет и какой день
# #     is_work, day = is_working_day(
# #         schedule_start_date=schedule_start_date,
# #         work_days=work_days,
# #         weekend_days=weekend_days,
# #         date=start_date,
# #         is_working=is_working,
# #         what_day=what_day,
# #     )
# #     return timetable_work(
# #         start=start_date,
# #         end=end_date,
# #         is_working=is_work,
# #         what_day=day,
# #         work_days=work_days,
# #         weekend_days=weekend_days,
# #
# #     )
#
#
# # if __name__ == "__main__":
# #     # test_schiduler()
# #     db = DB()
# #     excel = Excel("../test.xlsx")
# #
# #     days = 4
# #     other_date = datetime.now() + timedelta(days=days)
# #
# #     driver = next(drivers(db))
# #
# #     driver_schedule = get_timetable_period(
# #         schedule_start_date=datetime.now(),
# #         work_days=driver.schedule_type.work_days,
# #         weekend_days=driver.schedule_type.weekend_days,
# #         is_working=driver.work_schedule_history.is_working,
# #         what_day=driver.work_schedule_history.what_day,
# #         start_date=datetime.now(),
# #         end_date=other_date,
# #     )
# #     car_schedule = get_timetable_period(
# #         schedule_start_date=datetime.now(),
# #         is_working=True,
# #         what_day=1,
# #         work_days=-1,
# #         weekend_days=-1,
# #         start_date=datetime.now(),
# #         end_date=other_date,
# #     )
# #     # объединяем два расписания в одно
# #     combined_schedule = {}
# #     for car_day, driver_day in zip(car_schedule.items(), driver_schedule.items()):
# #         if car_day[1] == driver_day[1]:
# #             combined_schedule[car_day[0]] = driver.driver.name
# #         else:
# #             combined_schedule[car_day[0]] = car_day[1]
# #
# #     ic(driver)
# #     # ic(driver_schedule)
# #     ic(combined_schedule)
# #
# #
# #     # # создаем заголовок таблицы
# #     # title = ["Фамилия Имя Отчество"]
# #     # for day in range(days + 1):
# #     #     date = (other_date + timedelta(days=day)).strftime("%d-%m-%Y")
# #     #     title.append(date)
# #     # excel.add_row(title)
# #     #
# #     # # Заполняем таблицу построчно
# #     # for driver in drivers(db):
# #     #     schedule = get_timetable(
# #     #         driver.work_schedule_history.date,
# #     #         driver.schedule_type.work_days,
# #     #         driver.schedule_type.weekend_days,
# #     #         driver.work_schedule_history.is_working,
# #     #         driver.work_schedule_history.what_day,
# #     #         other_date,
# #     #         other_date + timedelta(days=days)
# #     #     )
# #     #     ic(driver)
# #     #     excel.add_row([driver.driver.name, *schedule.values()])  # ic(table)
# #     #
# #     # # выравнивание колонок
# #     # # ширина
# #     # excel.auto_alignment_column_width()
# #     # # равнение по центру
# #     # excel.auto_alignment_column_center()
# #     # # обрамление столбцов
# #     # excel.auto_border()
# #     # # сохраняем
# #     # excel.save()
