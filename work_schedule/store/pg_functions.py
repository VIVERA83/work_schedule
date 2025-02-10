from alembic.operations import Operations

from core.settings import PostgresSettings

pg_schema = PostgresSettings().postgres_schema  # noqa

pg_func_find_nearest_smaller_date = f"""
CREATE OR REPLACE FUNCTION {pg_schema}.find_nearest_smaller_date(passed_ts timestamp without time zone, driver_id integer)
 RETURNS jsonb
 LANGUAGE plpgsql
AS $function$
DECLARE 
	res jsonb;
BEGIN
	res:=(
	select 
		jsonb_build_object(
			'schedule_start_date', wsh."date",
			'work_days', st.work_days,
			'weekend_days', st.weekend_days,
			'is_working', wsh.is_working, 	
			'what_day', wsh.what_day
		)
	from work_schedule.work_schedule_history wsh
	join work_schedule.schedule_types st on st.id = wsh.id_schedule_type  
	where
		wsh.id_driver = driver_id    	
		and
    	passed_ts > wsh."date" and true 
	    or
    	passed_ts < wsh."date" and not true
order by abs(extract(epoch from passed_ts - wsh."date"))
limit 1
);
RETURN res;
END;
$function$;
"""

pg_func_all_ok = f"""
CREATE OR REPLACE FUNCTION {pg_schema}.all_ok(start_ts timestamp without time zone, stop_ts timestamp without time zone, driver_id integer)
 RETURNS jsonb[]
 LANGUAGE plpgsql
AS $function$
DECLARE 
	res jsonb[];
	smaller_date jsonb := work_schedule.find_nearest_smaller_date(start_ts, driver_id);
BEGIN
	res:= array((
	select 
    	    jsonb_build_object(
			'schedule_start_date', wsh."date",
			'work_days', st.work_days,
			'weekend_days', st.weekend_days,
			'is_working', wsh.is_working, 	
			'what_day', wsh.what_day		
		)
	from work_schedule.work_schedule_history wsh 
	join work_schedule.schedule_types st on st.id = wsh.id_schedule_type 
	where
		wsh.id_driver = driver_id    	
		and 
		wsh."date" BETWEEN start_ts AND stop_ts
group by wsh.date, st.work_days, st.weekend_days, wsh.is_working, wsh.what_day
));
IF smaller_date IS NOT NULL THEN
        res:= res || smaller_date;
    END IF;
RETURN res;
END;
$function$;
"""

pg_func_upper_column = f"""
CREATE OR REPLACE FUNCTION {pg_schema}.upper_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.name := UPPER(NEW.name);
    NEW.car_model := UPPER(NEW.car_model);
    NEW.car_number := UPPER(NEW.car_number);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

pg_func_upper_column_trigger = f"""
CREATE TRIGGER lower_column_trigger
BEFORE INSERT OR UPDATE ON work_schedule.car
FOR EACH ROW EXECUTE PROCEDURE {pg_schema}.lower_column();
"""


def create_pg_functions(op: Operations):
    """Создание функций для PostgresSQL"""

    op.execute(pg_func_find_nearest_smaller_date)
    op.execute(pg_func_all_ok)
    op.execute(pg_func_upper_column)
    op.execute(pg_func_upper_column_trigger)


def drop_pg_functions(op: Operations):
    """Удаление функций для PostgresSQL"""

    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.find_nearest_smaller_date;")
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.all_ok;")
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.upper_column;")
    op.execute(f"DROP TRIGGER IF EXISTS {pg_schema}.upper_column_trigger ON {pg_schema}.car;")
