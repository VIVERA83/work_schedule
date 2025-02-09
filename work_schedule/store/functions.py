f1 = """
CREATE OR REPLACE FUNCTION work_schedule.find_nearest_smaller_date(passed_ts timestamp without time zone, driver_id integer)
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
$function$
;
"""

f2 = """
CREATE OR REPLACE FUNCTION work_schedule.all_ok(start_ts timestamp without time zone, stop_ts timestamp without time zone, driver_id integer)
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
--order by abs(extract(epoch from start_ts - wsh."date"))
));
IF smaller_date IS NOT NULL THEN
        res:= res || smaller_date;
    END IF;
RETURN res;
END;
$function$
;
"""
f3 = """
CREATE OR REPLACE FUNCTION work_schedule.my_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM work_schedule.car_driver_association WHERE car_id = NEW.car_id) >= 3 THEN
        RAISE EXCEPTION 'Maximum number of links exceeded';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
# закрепляем триггер за таблицей car_driver_association
f4 = """
CREATE OR REPLACE TRIGGER my_trigger
BEFORE INSERT OR UPDATE ON work_schedule.car_driver_association
FOR EACH ROW
EXECUTE FUNCTION work_schedule.my_trigger_function()
"""