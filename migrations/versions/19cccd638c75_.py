"""empty message

Revision ID: 19cccd638c75
Revises: e861220c7499
Create Date: 2023-08-24 13:58:57.212584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '19cccd638c75'
down_revision = 'e861220c7499'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('post_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['author_id'], ['id'])
        batch_op.drop_column('author')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('post_ibfk_1', 'users', ['author'], ['id'])
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###