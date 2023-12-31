"""empty message

Revision ID: 7d38932628a6
Revises: 12804e175fa7
Create Date: 2023-12-24 17:07:14.047415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d38932628a6'
down_revision: Union[str, None] = '12804e175fa7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('tg_chat_username', sa.VARCHAR(length=256), nullable=True),
    sa.Column('tg_message_id', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.CHAR(length=26), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
