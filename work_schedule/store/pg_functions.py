from alembic.operations import Operations

from core.settings import PostgresSettings

pg_schema = PostgresSettings().postgres_schema  # noqa

# функция ищет минимальный день в диапазоне, в котором работает машина (водитель)
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

pg_func_get_employee_shifts_in_period = f"""
CREATE OR REPLACE FUNCTION {pg_schema}.get_employee_shifts_in_period(start_ts timestamp without time zone, stop_ts timestamp without time zone, driver_id integer)
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
BEFORE INSERT OR UPDATE ON {pg_schema}.car
FOR EACH ROW EXECUTE PROCEDURE {pg_schema}.upper_column();
"""

pg_func_check_crew_cars = f"""
CREATE OR REPLACE FUNCTION {pg_schema}.check_crew_cars()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM {pg_schema}.crew_cars WHERE id_crew = NEW.id_crew) >= 2 THEN
        RAISE EXCEPTION 'Too many cars in crew';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

pg_func_check_crew_cars_trigger = f"""
CREATE TRIGGER check_crew_cars_trigger
BEFORE INSERT OR UPDATE ON {pg_schema}.crew_cars
FOR EACH ROW EXECUTE PROCEDURE {pg_schema}.check_crew_cars();
"""

pg_func_check_crew_drivers = f"""
CREATE OR REPLACE FUNCTION {pg_schema}.check_crew_drivers()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM {pg_schema}.crew_drivers WHERE id_crew = NEW.id_crew) >= 3 THEN
        RAISE EXCEPTION 'Too many drivers in crew';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

pg_func_check_crew_drivers_trigger = f"""
CREATE TRIGGER check_crew_drivers_trigger
BEFORE INSERT OR UPDATE ON {pg_schema}.crew_drivers
FOR EACH ROW EXECUTE PROCEDURE {pg_schema}.check_crew_drivers();
"""

pg_func_get_car_shifts_in_period = f"""
-- суть функция выдает список смен типов графиков за указанный период по указанному машине
CREATE OR REPLACE FUNCTION {pg_schema}.get_car_shifts_in_period(start_ts timestamp without time zone, stop_ts timestamp without time zone, car_id integer)
 RETURNS jsonb[]
 LANGUAGE plpgsql
AS $function$
DECLARE 
	res jsonb[];
	smaller_date jsonb := {pg_schema}.find_nearest_smaller_date(start_ts, car_id);
BEGIN
	res:= array((
	select 
    	    jsonb_build_object(
			'schedule_start_date', csh."date",
			'work_days', st.work_days,
			'weekend_days', st.weekend_days,
			'is_working', csh.is_working, 	
			'what_day', csh.what_day		
		)
	from {pg_schema}.car_schedule_history csh 
	join {pg_schema}.schedule_types st on st.id = csh.id_schedule_type 
	where
		csh.id_car = car_id    	
		and 
		csh."date" BETWEEN start_ts AND stop_ts
group by csh.date, st.work_days, st.weekend_days, csh.is_working, csh.what_day
));
IF smaller_date IS NOT NULL THEN
        res:= res || smaller_date;
    END IF;
RETURN res;
END;
$function$
;
"""

pg_func_car_find_nearest_smaller_date = f"""
--функция возвращает минимальную дату начала графика работы машины, 
CREATE OR REPLACE FUNCTION {pg_schema}.car_find_nearest_smaller_date(passed_ts timestamp without time zone, car_id integer)
 RETURNS jsonb
 LANGUAGE plpgsql
AS $function$
DECLARE 
	res jsonb;
BEGIN
	res:=(
	select 
		jsonb_build_object(
			'schedule_start_date', csh."date",
			'work_days', st.work_days,
			'weekend_days', st.weekend_days,
			'is_working', csh.is_working, 	
			'what_day', csh.what_day
		)
	from {pg_schema}.car_schedule_history csh
	join {pg_schema}.schedule_types st on st.id = csh.id_schedule_type  
	where
		csh.id_car = car_id    	
		and
    	passed_ts > csh."date" and true 
	    or
    	passed_ts < csh."date" and not true
order by abs(extract(epoch from passed_ts - csh."date"))
limit 1
);
RETURN res;
END;
$function$
;
"""


def create_pg_functions(op: Operations):
    """Создание функций для PostgresSQL"""

    op.execute(pg_func_find_nearest_smaller_date)
    op.execute(pg_func_get_employee_shifts_in_period)
    op.execute(pg_func_upper_column)
    op.execute(pg_func_upper_column_trigger)
    op.execute(pg_func_check_crew_cars)
    op.execute(pg_func_check_crew_cars_trigger)
    op.execute(pg_func_check_crew_drivers)
    op.execute(pg_func_check_crew_drivers_trigger)
    op.execute(pg_func_get_car_shifts_in_period)
    op.execute(pg_func_car_find_nearest_smaller_date)


def drop_pg_functions(op: Operations):
    """Удаление функций для PostgresSQL"""

    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.find_nearest_smaller_date;")
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.get_employee_shifts_in_period;")
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.upper_column;")
    op.execute(
        f"DROP TRIGGER IF EXISTS {pg_schema}.upper_column_trigger ON {pg_schema}.car;"
    )
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.check_crew_cars;")
    op.execute(
        f"DROP TRIGGER IF EXISTS {pg_schema}.check_crew_cars_trigger ON {pg_schema}.crew_cars;"
    )
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.check_crew_drivers;")
    op.execute(
        f"DROP TRIGGER IF EXISTS {pg_schema}.check_crew_drivers_trigger ON {pg_schema}.crew_drivers;"
    )
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.get_car_shifts_in_period;")
    op.execute(f"DROP FUNCTION IF EXISTS {pg_schema}.car_find_nearest_smaller_date;")
