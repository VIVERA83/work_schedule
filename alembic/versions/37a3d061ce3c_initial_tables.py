"""Initial tables

Revision ID: 37a3d061ce3c
Revises: 
Create Date: 2025-02-10 20:06:06.948976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_function import PGFunction
from sqlalchemy import text as sql_text
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '37a3d061ce3c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('car_model', sa.String(), nullable=False),
    sa.Column('car_number', sa.String(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('car_number'),
    schema='work_schedule'
    )
    op.create_table('crew',
    sa.Column('cars', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('drivers', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='work_schedule'
    )
    op.create_table('driver',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='work_schedule'
    )
    op.create_table('schedule_types',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('work_days', sa.Integer(), nullable=False),
    sa.Column('weekend_days', sa.Integer(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='work_schedule'
    )
    op.create_index('type_index', 'schedule_types', ['name', 'work_days', 'weekend_days'], unique=True, schema='work_schedule')
    op.create_table('car_driver_association',
    sa.Column('car_id', sa.INTEGER(), nullable=False),
    sa.Column('driver_id', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['work_schedule.car.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['driver_id'], ['work_schedule.driver.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='work_schedule'
    )
    op.create_index('car_driver_association_index', 'car_driver_association', ['car_id', 'driver_id'], unique=True, schema='work_schedule')
    op.create_table('car_schedule_history',
    sa.Column('id_car', sa.INTEGER(), nullable=True),
    sa.Column('id_schedule_type', sa.INTEGER(), nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('is_working', sa.Boolean(), nullable=False),
    sa.Column('what_day', sa.Integer(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['id_car'], ['work_schedule.car.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_schedule_type'], ['work_schedule.schedule_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='work_schedule'
    )
    op.create_table('work_schedule_history',
    sa.Column('id_driver', sa.INTEGER(), nullable=True),
    sa.Column('id_schedule_type', sa.INTEGER(), nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('is_working', sa.Boolean(), nullable=False),
    sa.Column('what_day', sa.Integer(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['id_driver'], ['work_schedule.driver.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_schedule_type'], ['work_schedule.schedule_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='work_schedule'
    )
    work_schedule_my_trigger_function = PGFunction(
        schema="work_schedule",
        signature="my_trigger_function()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n    IF (SELECT COUNT(*) FROM work_schedule.car_driver_association WHERE car_id = NEW.car_id) >= 3 THEN\n        RAISE EXCEPTION 'Maximum number of links exceeded';\n    END IF;\n    RETURN NEW;\n    END;\n    $$ LANGUAGE plpgsql"
    )
    op.create_entity(work_schedule_my_trigger_function)

    work_schedule_find_nearest_smaller_date = PGFunction(
        schema="work_schedule",
        signature="find_nearest_smaller_date(passed_ts timestamp without time zone, driver_id integer)",
        definition='returns jsonb\n LANGUAGE plpgsql\nAS $function$\nDECLARE \n\tres jsonb;\nBEGIN\n\tres:=(\n\tselect \n\t\tjsonb_build_object(\n\t\t\t\'schedule_start_date\', wsh."date",\n\t\t\t\'work_days\', st.work_days,\n\t\t\t\'weekend_days\', st.weekend_days,\n\t\t\t\'is_working\', wsh.is_working, \t\n\t\t\t\'what_day\', wsh.what_day\n\t\t)\n\tfrom work_schedule.work_schedule_history wsh\n\tjoin work_schedule.schedule_types st on st.id = wsh.id_schedule_type  \n\twhere\n\t\twsh.id_driver = driver_id    \t\n\t\tand\n    \tpassed_ts > wsh."date" and true \n\t    or\n    \tpassed_ts < wsh."date" and not true\norder by abs(extract(epoch from passed_ts - wsh."date"))\nlimit 1\n);\nRETURN res;\nEND;\n$function$'
    )
    op.drop_entity(work_schedule_find_nearest_smaller_date)

    work_schedule_all_ok = PGFunction(
        schema="work_schedule",
        signature="all_ok(start_ts timestamp without time zone, stop_ts timestamp without time zone, driver_id integer)",
        definition='returns jsonb[]\n LANGUAGE plpgsql\nAS $function$\nDECLARE \n\tres jsonb[];\n\tsmaller_date jsonb := work_schedule.find_nearest_smaller_date(start_ts, driver_id);\nBEGIN\n\tres:= array((\n\tselect \n    \t    jsonb_build_object(\n\t\t\t\'schedule_start_date\', wsh."date",\n\t\t\t\'work_days\', st.work_days,\n\t\t\t\'weekend_days\', st.weekend_days,\n\t\t\t\'is_working\', wsh.is_working, \t\n\t\t\t\'what_day\', wsh.what_day\t\t\n\t\t)\n\tfrom work_schedule.work_schedule_history wsh \n\tjoin work_schedule.schedule_types st on st.id = wsh.id_schedule_type \n\twhere\n\t\twsh.id_driver = driver_id    \t\n\t\tand \n\t\twsh."date" BETWEEN start_ts AND stop_ts\ngroup by wsh.date, st.work_days, st.weekend_days, wsh.is_working, wsh.what_day\n--order by abs(extract(epoch from start_ts - wsh."date"))\n));\nIF smaller_date IS NOT NULL THEN\n        res:= res || smaller_date;\n    END IF;\nRETURN res;\nEND;\n$function$'
    )
    op.drop_entity(work_schedule_all_ok)
    op.execute(
        """CREATE OR REPLACE TRIGGER my_trigger
           BEFORE INSERT OR UPDATE ON work_schedule.car_driver_association
           FOR EACH ROW
           EXECUTE FUNCTION work_schedule.my_trigger_function()
        """
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    work_schedule_all_ok = PGFunction(
        schema="work_schedule",
        signature="all_ok(start_ts timestamp without time zone, stop_ts timestamp without time zone, driver_id integer)",
        definition='returns jsonb[]\n LANGUAGE plpgsql\nAS $function$\nDECLARE \n\tres jsonb[];\n\tsmaller_date jsonb := work_schedule.find_nearest_smaller_date(start_ts, driver_id);\nBEGIN\n\tres:= array((\n\tselect \n    \t    jsonb_build_object(\n\t\t\t\'schedule_start_date\', wsh."date",\n\t\t\t\'work_days\', st.work_days,\n\t\t\t\'weekend_days\', st.weekend_days,\n\t\t\t\'is_working\', wsh.is_working, \t\n\t\t\t\'what_day\', wsh.what_day\t\t\n\t\t)\n\tfrom work_schedule.work_schedule_history wsh \n\tjoin work_schedule.schedule_types st on st.id = wsh.id_schedule_type \n\twhere\n\t\twsh.id_driver = driver_id    \t\n\t\tand \n\t\twsh."date" BETWEEN start_ts AND stop_ts\ngroup by wsh.date, st.work_days, st.weekend_days, wsh.is_working, wsh.what_day\n--order by abs(extract(epoch from start_ts - wsh."date"))\n));\nIF smaller_date IS NOT NULL THEN\n        res:= res || smaller_date;\n    END IF;\nRETURN res;\nEND;\n$function$'
    )
    op.create_entity(work_schedule_all_ok)

    work_schedule_find_nearest_smaller_date = PGFunction(
        schema="work_schedule",
        signature="find_nearest_smaller_date(passed_ts timestamp without time zone, driver_id integer)",
        definition='returns jsonb\n LANGUAGE plpgsql\nAS $function$\nDECLARE \n\tres jsonb;\nBEGIN\n\tres:=(\n\tselect \n\t\tjsonb_build_object(\n\t\t\t\'schedule_start_date\', wsh."date",\n\t\t\t\'work_days\', st.work_days,\n\t\t\t\'weekend_days\', st.weekend_days,\n\t\t\t\'is_working\', wsh.is_working, \t\n\t\t\t\'what_day\', wsh.what_day\n\t\t)\n\tfrom work_schedule.work_schedule_history wsh\n\tjoin work_schedule.schedule_types st on st.id = wsh.id_schedule_type  \n\twhere\n\t\twsh.id_driver = driver_id    \t\n\t\tand\n    \tpassed_ts > wsh."date" and true \n\t    or\n    \tpassed_ts < wsh."date" and not true\norder by abs(extract(epoch from passed_ts - wsh."date"))\nlimit 1\n);\nRETURN res;\nEND;\n$function$'
    )
    op.create_entity(work_schedule_find_nearest_smaller_date)

    work_schedule_my_trigger_function = PGFunction(
        schema="work_schedule",
        signature="my_trigger_function()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n    IF (SELECT COUNT(*) FROM work_schedule.car_driver_association WHERE car_id = NEW.car_id) >= 3 THEN\n        RAISE EXCEPTION 'Maximum number of links exceeded';\n    END IF;\n    RETURN NEW;\n    END;\n    $$ LANGUAGE plpgsql"
    )
    op.drop_entity(work_schedule_my_trigger_function)

    op.drop_table('work_schedule_history', schema='work_schedule')
    op.drop_table('car_schedule_history', schema='work_schedule')
    op.drop_index('car_driver_association_index', table_name='car_driver_association', schema='work_schedule')
    op.drop_table('car_driver_association', schema='work_schedule')
    op.drop_index('type_index', table_name='schedule_types', schema='work_schedule')
    op.drop_table('schedule_types', schema='work_schedule')
    op.drop_table('driver', schema='work_schedule')
    op.drop_table('crew', schema='work_schedule')
    op.drop_table('car', schema='work_schedule')
    # ### end Alembic commands ###
