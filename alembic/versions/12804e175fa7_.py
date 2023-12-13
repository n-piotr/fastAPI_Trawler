"""empty message

Revision ID: 12804e175fa7
Revises: 4f8816e2b136
Create Date: 2023-12-13 14:36:50.452773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '12804e175fa7'
down_revision: Union[str, None] = '4f8816e2b136'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('settings', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.drop_column('users', 'keywords')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('keywords', sa.VARCHAR(length=256), autoincrement=False, nullable=True))
    op.drop_column('users', 'settings')
    # ### end Alembic commands ###
