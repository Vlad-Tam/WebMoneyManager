"""Update user table to fastapi_users

Revision ID: f28930f9930e
Revises: 8132c076eed3
Create Date: 2024-08-28 12:25:20.417950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f28930f9930e'
down_revision: Union[str, None] = '8132c076eed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('is_superuser', sa.Boolean(), nullable=False))
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'is_verified')
    op.drop_column('user', 'is_superuser')
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###
