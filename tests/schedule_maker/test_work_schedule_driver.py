from collections import defaultdict
from datetime import datetime

from icecream import ic

from tests.schedule_maker.data import (driver_0_s, driver_1_s,

                                       today_1, date_17_01_2025, \
                                       date_06_01_2025, driver_2_s)

from work_schedule.store.scheduler.schedule_maker import ScheduleMaker
from work_schedule.store.scheduler.utils import SIGNAL_WORK


# driver_schedules_0 = {
#     0: driver_0_s,
#     1: driver_1_s,
# }
# 
# car_schedules_0 = {
#     0: car_0_s,
#     1: car_1_s,
# }
# relationships_0 = {
#     0: [0, 1],
#     1: [0, 1],
# }
# 
# 
# work = WorkScheduleDriver(driver_schedules_0, car_schedules_0, relationships_0)
# 
# work.create(today_1, date_17_01_2025)

def marge_schedule_makers(start_date: datetime, end_date: datetime, *schedule_makers: ScheduleMaker):
    s = {schedule_maker.name: schedule_maker.make_schedule(start_date=start_date, end_date=end_date) for schedule_maker
         in
         schedule_makers}

    return s.values()


def schedule_generator(schedule_maker: ScheduleMaker, start_date: datetime, end_date: datetime):
    next_date = None
    buffer = None
    for date, signal in schedule_maker.make_schedule(start_date=start_date, end_date=end_date).items():
        if next_date is not None:
            buffer = next_date
        if buffer is not None and datetime.strptime(buffer, '%d-%m-%Y') > datetime.strptime(date, '%d-%m-%Y'):
            continue
        next_date = (yield date, signal)


def test_schedule_generator():
    # ic(driver_0_s.make( today_1, date_17_01_2025))
    # ic(driver_1_s.make( today_1, date_17_01_2025))
    gen_0 = schedule_generator(driver_0_s, today_1, date_17_01_2025)
    gen_1 = schedule_generator(driver_1_s, today_1, date_17_01_2025)
    gens = [gen_1, gen_0]
    date = None
    index = 0
    max_index = len(gens)
    table = {}
    signal = None

    for ind, (d, signal) in enumerate([next(gen) for gen in gens]):
        if signal == SIGNAL_WORK:
            table[d] = ind
            index = ind
            date = d
            break

    while True:
        try:
            date, signal = gens[index].send(date)
            if signal == SIGNAL_WORK:
                table[date] = index
                continue
            else:
                index = index + 1 if index + 1 < max_index else 0
        except StopIteration:
            break

    ic(table)


def test_schedule_version_1():
    # test_schedule_generator()
    gen_0 = driver_0_s.make_schedule_generator(today_1, date_17_01_2025)
    gen_1 = driver_1_s.make_schedule_generator(today_1, date_17_01_2025)
    gens = [gen_0, gen_1]

    date = None
    index = 0
    max_index = len(gens)
    table = {}
    buffer = defaultdict(dict)
    signal = None
    old = None

    for ind, (d, signal) in enumerate([next(gen) for gen in gens]):
        if signal == SIGNAL_WORK:
            table[d] = ind
            index = ind
            date = d
            old = d
            break

    while True:
        try:
            old = date
            date, signal = gens[index].send(date)
            if signal == SIGNAL_WORK:
                table[date] = index
                continue
            else:
                for i, gen in enumerate(gens):
                    if i != index:
                        d, s = gen.send(old)
                        if s == SIGNAL_WORK:
                            buffer[d].update({i: s})
                index = index + 1 if index + 1 < max_index else 0
        except StopIteration:
            break

    ic(table, buffer)


def test_schedule_version_2(start: datetime, end: datetime, *schedule_makers: ScheduleMaker):
    gens = {schedule_maker.name: schedule_maker.make_schedule_generator(start, end) for schedule_maker in
            schedule_makers}
    current_id = list(gens.keys())[0]
    current_index = 0
    date = None
    table = {}
    buffer = defaultdict(dict)
    my_signal = "P"

    while True:
        try:
            for index, (id_, gen) in enumerate(gens.items()):
                date, signal = next(gen)

                if current_id == id_ and signal == SIGNAL_WORK:
                    table[date] = current_id
                    current_index = index
                elif signal == SIGNAL_WORK:
                    buffer[date][id_] = signal

            if table.get(date, None) is None:
                if buffer_data := buffer.get(date, None):
                    print(date, buffer_data)
                    indexs = {list(gens.keys()).index(id_): [id_, s] for id_, s in buffer_data.items()}

                    for ind, (id_, s) in indexs.items():

                        if ind > current_index:
                            current_id = id_
                            break

                    if buffer_data.get(current_id, None) is None:
                        print(date, current_index, indexs)
                        current_id = indexs[list(indexs.keys())[0]][0]
                    buffer_data.pop(current_id)
                    table[date] = current_id

                    if not buffer.get(date, None):
                        buffer.pop(date)

                else:
                    table[date] = my_signal
        except StopIteration:
            break
    ic(table, buffer)


def test_schedule_version_3(start: datetime, end: datetime, *schedule_makers: ScheduleMaker):
    base_schedule_maker = ScheduleMaker(
        "Car",
        datetime(year=2025, month=1, day=1),
        5,
        2,
        True,
        1,
    )
    test_scheduler_car = base_schedule_maker.make_schedule_generator(start, end)
    ic(base_schedule_maker.make_schedule(start, end))

    gens = {schedule_maker.name: schedule_maker.make_schedule_generator(start, end) for schedule_maker in
            schedule_makers}
    current_id = list(gens.keys())[0]
    current_index = 0
    date = None
    table = {}
    buffer = defaultdict(dict)


    while True:
        try:
            car_date, car_signal = next(test_scheduler_car)
            print(car_date, car_signal, car_signal == SIGNAL_WORK)
            if car_signal == SIGNAL_WORK:
                for index, (id_, gen) in enumerate(gens.items()):
                    date, signal = next(gen)

                    if current_id == id_ and signal == SIGNAL_WORK:
                        table[date] = current_id
                        current_index = index
                    elif signal == SIGNAL_WORK:
                        buffer[date][id_] = signal

                if table.get(date, None) is None:
                    if buffer_data := buffer.get(date, None):

                        indexs = {list(gens.keys()).index(id_): [id_, s] for id_, s in buffer_data.items()}

                        for ind, (id_, s) in indexs.items():

                            if ind > current_index:
                                current_id = id_
                                break

                        if buffer_data.get(current_id, None) is None:

                            current_id = indexs[list(indexs.keys())[0]][0]
                        buffer_data.pop(current_id)
                        table[date] = current_id

                        if not buffer.get(date, None):
                            buffer.pop(date)

                    else:
                        # table[date] = my_signal
                        table[car_date] = car_signal
            else:
                table[car_date] = car_signal
                for index, (id_, gen) in enumerate(gens.items()):
                    date, signal = next(gen)
                    if signal == SIGNAL_WORK:
                        buffer[date][id_] = signal
        except StopIteration:
            break
    ic(table, buffer)


def test_schedule_version_4(start: datetime, end: datetime, *schedule_makers: ScheduleMaker):
    base_schedule_maker = ScheduleMaker(
        "Car",
        datetime(year=2025, month=1, day=1),
        5,
        2,
        True,
        1,
    )
    test_scheduler_car = base_schedule_maker.make_schedule_generator(start, end)


    gens = {schedule_maker.name: schedule_maker.make_schedule_generator(start, end) for schedule_maker in
            schedule_makers}
    current_id = list(gens.keys())[0]
    current_index = 0
    date = None
    table = {}
    buffer = defaultdict(dict)

    while True:
        try:
            car_date, car_signal = next(test_scheduler_car)

            if car_signal == SIGNAL_WORK:
                for index, (id_, gen) in enumerate(gens.items()):
                    date, signal = next(gen)

                    if current_id == id_ and signal == SIGNAL_WORK:
                        table[date] = current_id
                        current_index = index
                    elif signal == SIGNAL_WORK:
                        buffer[date][id_] = signal

                if table.get(date, None) is None:
                    if buffer_data := buffer.get(date, None):

                        indexs = {list(gens.keys()).index(id_): [id_, s] for id_, s in buffer_data.items()}

                        for ind, (id_, s) in indexs.items():

                            if ind > current_index:
                                current_id = id_
                                break

                        if buffer_data.get(current_id, None) is None:
                            current_id = indexs[list(indexs.keys())[0]][0]
                        buffer_data.pop(current_id)
                        table[date] = current_id

                        if not buffer.get(date, None):
                            buffer.pop(date)

                    else:
                        table[car_date] = car_signal
            else:
                table[car_date] = car_signal
                for index, (id_, gen) in enumerate(gens.items()):
                    date, signal = next(gen)
                    if signal == SIGNAL_WORK:
                        buffer[date][id_] = signal
        except StopIteration:
            break
    return table, buffer

if __name__ == '__main__':
    result = test_schedule_version_4(
        date_06_01_2025,
        date_17_01_2025,
        driver_0_s,
        driver_1_s,
        driver_2_s,
    )
    ic(result[0])
    ic(result[1])
    # test_schedule_version_2(
    #     date_06_01_2025,
    #     date_17_01_2025,
    #     driver_0_s,
    #     driver_1_s,
    #     driver_2_s,
    # )

    #
    # old = date
    # date, signal = gens[current_id].send(date)
    #
    # for id_, gen in gens.items():
    #     if id_ != current_id:
    #         d, s = gen.send(old)
    #         if s == SIGNAL_WORK:
    #             buffer[d][id_] = s
    #
    # if signal == SIGNAL_WORK:
    #     table[date] = current_id
    #
    # elif buffer_data := buffer.get(old, None):
    #     index = ids.index(current_id)
    #     indexs = {list(gens.keys()).index(id_): [id_, s] for id_, s in buffer_data.items()}
    #     for ind in indexs:
    #         if ind > index:
    #
    #
    #
    #     id___ = list(buffer_data.keys())
    #     table[old] = id___
    #     buffer_data.pop(id___)
    #     if not buffer[old]:
    #         buffer.pop(old)
    # # continue
    # else:
    #     index = ids.index(current_id)
    #     current_id = ids[index + 1] if index + 1 < count_ids else ids[0]

    # except StopIteration:
    #     break
    # print()
    # print("table")
    # print(*[i for i in table.items()], sep='\n')
    # print("buffer")
    # print(*[i for i in buffer.items()], sep='\n')
    # u = {'11-01-2025': {1: 'P', 2: 'P'}}
    # a, *b =u.get('11-01-2025')
    # ic(a,b)
    # фиксация
    # # test_schedule_generator()
    # gen_0 = driver_0_s.make_schedule_generator(today_1, date_17_01_2025)
    # gen_1 = driver_1_s.make_schedule_generator(today_1, date_17_01_2025)
    # gen_2 = driver_1_s.make_schedule_generator(today_1, date_17_01_2025)
    # gens = [gen_0, gen_1, gen_2]
    #
    # date = None
    # index = 0
    # max_index = len(gens)
    # table = {}
    # buffer = defaultdict(dict)
    # signal = None
    # old = None
    #
    # for ind, (d, signal) in enumerate([next(gen) for gen in gens]):
    #     if signal == SIGNAL_WORK:
    #         table[d] = ind
    #         index = ind
    #         date = d
    #         old = d
    #         break
    #
    # while True:
    #     try:
    #         old = date
    #         date, signal = gens[index].send(date)
    #         if signal == SIGNAL_WORK:
    #             table[date] = index
    #             for i, gen in enumerate(gens):
    #                 if i != index:
    #                     d, s = gen.send(old)
    #                     if s == SIGNAL_WORK:
    #                         buffer[d].update({i: s})
    #             if not table.get(old, None) and buffer.get(old, None):
    #                 i, *_ = buffer.get(old)
    #                 table[old] = i
    #             continue
    #         else:
    #
    #             index = index + 1 if index + 1 < max_index else 0
    #
    #     except StopIteration:
    #         break
    #
    # ic(table, buffer)
    # while True:
    #     try:
    #         if date == "09-01-2025":
    #             date, signal = gen_1.send("16-01-2025")
    #         else:
    #             date, signal = next(gen_1)
    #         print(date, signal)
    #     except StopIteration:
    #         break

# result = marge_schedule_makers(today_1, date_17_01_2025, car_0_s, driver_0_s, driver_1_s)
# ic(result)
