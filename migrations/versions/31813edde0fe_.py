"""empty message

Revision ID: 31813edde0fe
Revises: None
Create Date: 2015-02-05 22:10:05.296721

"""

# revision identifiers, used by Alembic.
revision = '31813edde0fe'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('feed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=True),
    sa.Column('url', sa.String(length=120), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feed_url'), 'feed', ['url'], unique=True)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=True),
    sa.Column('link', sa.String(length=120), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('author', sa.String(length=120), nullable=True),
    sa.Column('summary', sa.String(length=500), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_item_link'), 'item', ['link'], unique=True)
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('subscriptions',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=True),
    sa.Column('mergeable', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    op.drop_table('roles_users')
    op.drop_index(op.f('ix_item_link'), table_name='item')
    op.drop_table('item')
    op.drop_index(op.f('ix_feed_url'), table_name='feed')
    op.drop_table('feed')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('role')
    ### end Alembic commands ###