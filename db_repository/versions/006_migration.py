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

subscriptions = Table('subscriptions', post_meta,
    Column('user_id', Integer),
    Column('feed_id', Integer),
    Column('mergeable', Boolean),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feed'].create()
    post_meta.tables['subscriptions'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['feed'].drop()
    post_meta.tables['subscriptions'].drop()
    post_meta.tables['user'].drop()
