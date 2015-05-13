"""empty message

Revision ID: 1d3f7409e3b9
Revises: 2780dc80a7c0
Create Date: 2015-05-13 14:43:05.065155

"""

# revision identifiers, used by Alembic.
revision = '1d3f7409e3b9'
down_revision = '2780dc80a7c0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feed', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_count', sa.Integer(), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feed', schema=None) as batch_op:
        batch_op.drop_column('item_count')

    ### end Alembic commands ###
