from black.trans import defaultdict
from icecream import ic

data = [
    ("о695рс196", "Филатов Александр Алексеевич"),
    ("о695рс196", "Миронов Михаил Викторович"),
    ("о123рс196", "Яшин Александр Кириллович"),
    ("о123рс196", "Филатов Александр Алексеевич"),
    ("о123рс196", "Миронов Михаил Викторович"),
    ("К111ММ755", "Незнайкин Незнайка Михайлович"),
]
result_car = defaultdict(list)
result_driver = defaultdict(list)
for car_number, worker_name in data:
    result_car[car_number].append(worker_name)
    result_driver[worker_name].append(car_number)

ic(result_car, result_driver)


r = defaultdict(list)
for car_number, drivers in result_car.items():
    # создаем WorkerSchedule на машину.

    1

# em = defaultdict(dict)
# for driver, cars in result_driver.items():
#
#     for dr in result_driver:
#         if result_driver[dr] == cars:
#             em[ek][0].add(dr)
#             print(set(result_driver[dr]),em[ek][1])
#              em[ek][1].update(set(result_driver[dr]))
#


# ic(em)
