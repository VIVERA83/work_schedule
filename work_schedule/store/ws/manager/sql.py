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
