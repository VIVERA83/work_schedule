"""Initial tables

Revision ID: 3b197158fa33
Revises: 
Create Date: 2025-01-19 17:34:24.919191

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3b197158fa33"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "car",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("car_model", sa.String(), nullable=False),
        sa.Column("car_number", sa.String(), nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("car_number"),
        schema="work_schedule",
    )
    op.create_table(
        "driver",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="work_schedule",
    )
    op.create_table(
        "schedule_types",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("work_days", sa.Integer(), nullable=False),
        sa.Column("weekend_days", sa.Integer(), nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="work_schedule",
    )
    op.create_index(
        "type_index",
        "schedule_types",
        ["name", "work_days", "weekend_days"],
        unique=True,
        schema="work_schedule",
    )
    op.create_table(
        "car_driver_association",
        sa.Column("car_id", sa.INTEGER(), nullable=False),
        sa.Column("driver_id", sa.INTEGER(), nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["car_id"], ["work_schedule.car.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["driver_id"], ["work_schedule.driver.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="work_schedule",
    )
    op.create_index(
        "car_driver_association_index",
        "car_driver_association",
        ["car_id", "driver_id"],
        unique=True,
        schema="work_schedule",
    )
    op.create_table(
        "work_schedule_history",
        sa.Column("id_driver", sa.INTEGER(), nullable=True),
        sa.Column("id_schedule_type", sa.INTEGER(), nullable=True),
        sa.Column(
            "date",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("is_working", sa.Boolean(), nullable=False),
        sa.Column("what_day", sa.Integer(), nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.ForeignKeyConstraint(
            ["id_driver"], ["work_schedule.driver.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["id_schedule_type"],
            ["work_schedule.schedule_types.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="work_schedule",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("work_schedule_history", schema="work_schedule")
    op.drop_index(
        "car_driver_association_index",
        table_name="car_driver_association",
        schema="work_schedule",
    )
    op.drop_table("car_driver_association", schema="work_schedule")
    op.drop_index("type_index", table_name="schedule_types", schema="work_schedule")
    op.drop_table("schedule_types", schema="work_schedule")
    op.drop_table("driver", schema="work_schedule")
    op.drop_table("car", schema="work_schedule")
    # ### end Alembic commands ###
