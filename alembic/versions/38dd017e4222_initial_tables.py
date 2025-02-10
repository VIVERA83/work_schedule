"""Initial tables

Revision ID: 38dd017e4222
Revises: 
Create Date: 2025-02-10 22:44:34.246022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from store.pg_functions import create_pg_functions, drop_pg_functions

# revision identifiers, used by Alembic.
revision: str = '38dd017e4222'
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
    op.create_table('crew_cars',
    sa.Column('id_crew', sa.INTEGER(), nullable=False),
    sa.Column('id_car', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['id_car'], ['work_schedule.car.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_crew'], ['work_schedule.crew.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_car'),
    schema='work_schedule'
    )
    op.create_table('crew_drivers',
    sa.Column('id_crew', sa.INTEGER(), nullable=False),
    sa.Column('id_driver', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['id_crew'], ['work_schedule.crew.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_driver'], ['work_schedule.driver.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_driver'),
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
    # ### end Alembic commands ###
    # создания функций для PostgresSQL
    create_pg_functions(op)

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('work_schedule_history', schema='work_schedule')
    op.drop_table('crew_drivers', schema='work_schedule')
    op.drop_table('crew_cars', schema='work_schedule')
    op.drop_table('car_schedule_history', schema='work_schedule')
    op.drop_index('type_index', table_name='schedule_types', schema='work_schedule')
    op.drop_table('schedule_types', schema='work_schedule')
    op.drop_table('driver', schema='work_schedule')
    op.drop_table('crew', schema='work_schedule')
    op.drop_table('car', schema='work_schedule')

    # ### end Alembic commands ###
    # удаление функций для PostgresSQL
    drop_pg_functions(op)