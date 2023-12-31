"""empty message

Revision ID: 1216c9ca5ee8
Revises: 
Create Date: 2023-12-06 20:16:41.468117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1216c9ca5ee8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.SMALLINT(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=32), nullable=False),
    sa.Column('slug', sa.VARCHAR(length=32), nullable=False),
    sa.CheckConstraint("slug not like '%% %%'"),
    sa.CheckConstraint('length(name) >= 2'),
    sa.CheckConstraint('length(slug) >= 2'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('users',
    sa.Column('id', sa.CHAR(length=26), nullable=False),
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('password', sa.CHAR(length=60), nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('is_staff', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=256), nullable=False),
    sa.Column('body', sa.VARCHAR(length=3000), nullable=False),
    sa.Column('tg_link', sa.VARCHAR(length=256), nullable=True),
    sa.Column('date_created', sa.TIMESTAMP(), nullable=False),
    sa.Column('category_id', sa.SMALLINT(), nullable=False),
    sa.CheckConstraint('length(body) >= 50'),
    sa.CheckConstraint('length(title) >= 2'),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], onupdate='CASCADE', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
