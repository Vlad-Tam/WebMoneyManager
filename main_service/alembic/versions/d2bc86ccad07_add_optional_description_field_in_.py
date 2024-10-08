"""Add optional description field in transaction_table

Revision ID: d2bc86ccad07
Revises: 97bedfd52369
Create Date: 2024-08-15 23:24:38.960520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd2bc86ccad07'
down_revision: Union[str, None] = '97bedfd52369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transaction', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('transaction', 'operation_type',
               existing_type=postgresql.ENUM('add', 'sub', name='transaction_type'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transaction', 'operation_type',
               existing_type=postgresql.ENUM('add', 'sub', name='transaction_type'),
               nullable=True)
    op.alter_column('transaction', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
