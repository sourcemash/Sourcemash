"""empty message

Revision ID: 2780dc80a7c0
Revises: 293250007b39
Create Date: 2015-05-07 14:15:50.002172

"""

# revision identifiers, used by Alembic.
revision = '2780dc80a7c0'
down_revision = '293250007b39'

from alembic import op
import sqlalchemy as sa


def upgrade():

    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feed', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_feed_url'))
        batch_op.add_column(sa.Column('public', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_feed_url'), 'feed', ['url'], unique=True)


    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('feed', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_feed_url'))
        batch_op.drop_column('public')
    op.create_index(op.f('ix_feed_url'), 'feed', ['url'], unique=True)
    ### end Alembic commands ###
