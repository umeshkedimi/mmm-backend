"""remove server defaults from users

Revision ID: 28eefe992ab3
Revises: 4c7b955be50c
Create Date: 2025-06-01 00:47:43.709580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28eefe992ab3'
down_revision: Union[str, None] = '4c7b955be50c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'password_hash', server_default=None)


def downgrade() -> None:
    op.alter_column('users', 'password_hash', server_default='dummy')
