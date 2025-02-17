from datetime import datetime

from sqlalchemy import text, TextClause

SQL_QUERY_STRING = str
sql_query_current_worker_schedule = """
select
d."name",
wsh."date" as schedule_start_date,
st.work_days,
st.weekend_days,
wsh.is_working,
wsh.what_day 
from work_schedule.driver d
join work_schedule.work_schedule_history wsh on wsh.id = d.id
join work_schedule.schedule_types st on st.id = wsh.id_schedule_type 
where d.id = :driver_id
order by wsh.date desc
;
"""


def get_sql_query_crews(pg_schema: str, start_date: datetime, end_date: datetime) -> TextClause:
    """Получить SQL запрос, который возвращает экипаж из машин и водителей.

    :param pg_schema: Postgres схема
    :param start_date: Стартовая дата для сбора графиков смен
    :param end_date: Последняя дата для сбора смен
    :return: SQL_QUERY_STRING
    """
    return text(f"""
select 
c.id,
array_agg( 
	DISTINCT
	jsonb_build_object(
		'id', c2.id,
		'name', c2."name",
		'model', c2.car_model,
		'number', c2.car_number,
		'schedules', {pg_schema}.get_car_shifts_in_period('{start_date}','{end_date}',c2.id)
		)
	) as cars,
array_agg(
	DISTINCT
	jsonb_build_object(
		'id',d.id,
		'name', d."name",
		'schedules', {pg_schema}.get_employee_shifts_in_period('{start_date}','{end_date}',d.id)
		)
	) as drivers
from 
{pg_schema}.crew c
join {pg_schema}.crew_cars cc on cc.id_crew = c.id 
join {pg_schema}.car c2 on c2.id = cc.id_car
join {pg_schema}.crew_drivers cd on cd.id_crew  = c.id
join {pg_schema}.driver d on d.id = cd.id_driver 
group by c.id
;
""")
