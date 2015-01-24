from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
feed = Table('feed', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=250)),
    Column('url', String(length=120)),
    Column('last_updated', DateTime),
)

item = Table('item', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=250)),
    Column('url', String(length=120)),
    Column('publication_date', DateTime),
    Column('author', String(length=120)),
    Column('category', String(length=120)),
    Column('description', String(length=500)),
    Column('feed_id', Integer),
)

role = Table('role', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=80)),
)

roles_users = Table('roles_users', post_meta,
    Column('user_id', Integer),
    Column('role_id', Integer),
)

subscriptions = Table('subscriptions', post_meta,
    Column('user_id', Integer),
    Column('feed_id', Integer),
    Column('mergeable', Boolean),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
    Column('password', String(length=255)),
    Column('active', Boolean),
    Column('confirmed_at', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feed'].create()
    post_meta.tables['item'].create()
    post_meta.tables['role'].create()
    post_meta.tables['roles_users'].create()
    post_meta.tables['subscriptions'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feed'].drop()
    post_meta.tables['item'].drop()
    post_meta.tables['role'].drop()
    post_meta.tables['roles_users'].drop()
    post_meta.tables['subscriptions'].drop()
    post_meta.tables['user'].drop()
