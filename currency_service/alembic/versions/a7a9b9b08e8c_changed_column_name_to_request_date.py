"""Changed column name to request_date

Revision ID: a7a9b9b08e8c
Revises: 1fd0be684952
Create Date: 2024-08-24 12:27:18.863761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7a9b9b08e8c'
down_revision: Union[str, None] = '1fd0be684952'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exchange_rate', sa.Column('request_date', sa.Date(), nullable=False))
    op.drop_index('ix_exchange_rate_date', table_name='exchange_rate')
    op.create_index(op.f('ix_exchange_rate_request_date'), 'exchange_rate', ['request_date'], unique=False)
    op.drop_column('exchange_rate', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exchange_rate', sa.Column('date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_exchange_rate_request_date'), table_name='exchange_rate')
    op.create_index('ix_exchange_rate_date', 'exchange_rate', ['date'], unique=False)
    op.drop_column('exchange_rate', 'request_date')
    # ### end Alembic commands ###
