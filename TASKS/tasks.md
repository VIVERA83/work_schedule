1. сделать запрос к БД который бы возвращал данные для формирования графика сменности и наряда
```sql
select array_agg(
               DISTINCT
               jsonb_build_object(
                       'id', c2.id,
                       'name', c2."name",
                       'model', c2.car_model,
                       'number', c2.car_number
               )
       ) as cars,
       array_agg(
               DISTINCT
               jsonb_build_object(
                       'id', d.id,
                       'name', d."name"
               )
       ) as drivers
from work_schedule.crew c
         join work_schedule.crew_cars cc on cc.id_crew = c.id
         join work_schedule.car c2 on c2.id = cc.id_car
         join work_schedule.crew_drivers cd on cd.id_crew = c.id
         join work_schedule.driver d on d.id = cd.id_driver
group by c.id
;
```
Это запрос возвращает экипажи с их машинами. 
Теперь нужно добавить в запрос добавить по водителям и машинам их графики сменности, 
причем нужно будет добавлять только те которые актуальный в тот промежуток в который будет строиться наряд.

__Выполнено, добавлено.__

17-02-2025

        - Доработан запрос к БД, теперь дополнительно выводится id экипажа.
        - создан api метод get_all_crews - он возвращает list[CrewSchema]
        
        - начал делать [scheduler](../work_schedule/store/scheduler).

18-02-2025

    - нахожусь в [views.py](../work_schedule/api/worker_schedule/views.py)
    - делается файил ескель
    - нужно все облагородить

2. Теперь нужно генерировать график с помощью [scheduler](../work_schedule/store/scheduler).
3. Далее этот график записывать в excel 
4. Далее это график возвращать клиенту (тому кто прислал запрос)
