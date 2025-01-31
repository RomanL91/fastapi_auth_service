"""Drop clientuuids table

Revision ID: 529f7c22ec85
Revises: 3d02d8fdefd6
Create Date: 2025-01-16 00:41:17.106045

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "529f7c22ec85"
down_revision: Union[str, None] = "3d02d8fdefd6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
