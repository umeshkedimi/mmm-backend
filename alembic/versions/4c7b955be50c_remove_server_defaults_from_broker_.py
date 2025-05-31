"""remove server defaults from broker_accounts

Revision ID: 4c7b955be50c
Revises: 0d5b15618766
Create Date: 2025-06-01 00:43:44.211237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c7b955be50c'
down_revision: Union[str, None] = '0d5b15618766'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('broker_accounts', 'broker_name', server_default=None)
    op.alter_column('broker_accounts', 'client_id', server_default=None)
    op.alter_column('broker_accounts', 'access_token', server_default=None)
    op.alter_column('broker_accounts', 'telegram_chat_id', server_default=None)
    op.alter_column('broker_accounts', 'lot_size', server_default=None)
    op.alter_column('broker_accounts', 'index', server_default=None)
    op.alter_column('broker_accounts', 'direction', server_default=None)
    op.alter_column('broker_accounts', 'user_id', server_default=None)


def downgrade() -> None:
    op.alter_column('broker_accounts', 'broker_name', server_default='dhan')
    op.alter_column('broker_accounts', 'client_id', server_default='dummy')
    op.alter_column('broker_accounts', 'access_token', server_default='dummy')
    op.alter_column('broker_accounts', 'telegram_chat_id', server_default='dummy')
    op.alter_column('broker_accounts', 'lot_size', server_default='15')
    op.alter_column('broker_accounts', 'index', server_default='banknifty')
    op.alter_column('broker_accounts', 'direction', server_default='sell')
    op.alter_column('broker_accounts', 'user_id', server_default='1')
