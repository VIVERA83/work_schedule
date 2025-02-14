"""Initial functions

Revision ID: 2
Revises:
Create Date: 2025-02-13 21:46:02.334698

"""

from typing import Sequence, Union

from alembic import op


from store.pg_functions import create_pg_functions, drop_pg_functions

# revision identifiers, used by Alembic.
revision: str = "2"
down_revision: Union[str, None] = "1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    create_pg_functions(op)


def downgrade() -> None:
    drop_pg_functions(op)
