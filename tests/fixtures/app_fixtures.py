import pytest
from rq import SimpleWorker, Queue
from rq import push_connection, pop_connection

from sourcemash import create_app
from worker import create_worker
from sourcemash.database import db as _db
from sourcemash.mail import mail
from tests.factories import (feed_factories, item_factories, role_factories,
                             category_factories, user_factories,
                             user_item_factories, user_feed_factories,
                             user_category_factories)


@pytest.yield_fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application"""
    app = create_app("testing")

    # Establish an application context before running the tests.
    ctx = app.test_request_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app, request):
    """Session-wide test database"""

    _db.drop_all()
    _db.create_all()
    _db.app = app

    yield _db


@pytest.yield_fixture(autouse=True)
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options)
    db.session = session

    feed_factories.FeedFactory._meta.sqlalchemy_session = session
    feed_factories.TechCrunchFeedFactory._meta.sqlalchemy_session = session
    user_factories.UserFactory._meta.sqlalchemy_session = session
    item_factories.ItemFactory._meta.sqlalchemy_session = session
    category_factories.CategoryFactory._meta.sqlalchemy_session = session
    user_item_factories.UserItemFactory._meta.sqlalchemy_session = session
    user_item_factories.UserItemUpvoteFactory._meta.sqlalchemy_session = session
    user_item_factories.UserItemDownvoteFactory._meta.sqlalchemy_session = session
    user_item_factories.UserItemReadFactory._meta.sqlalchemy_session = session
    user_item_factories.UserItemSavedFactory._meta.sqlalchemy_session = session
    user_feed_factories.UserFeedFactory._meta.sqlalchemy_session = session
    user_category_factories.UserCategoryFactory._meta.sqlalchemy_session = session
    item_factories.EbolaItemFactory._meta.sqlalchemy_session = session
    role_factories.RoleFactory._meta.sqlalchemy_session = session

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture()
def test_client(app, request):
    with app.test_client() as client:
        yield client


@pytest.yield_fixture()
def connection(request):
    push_connection(create_worker())
    yield
    pop_connection()


@pytest.yield_fixture()
def worker(connection, request):
    email = Queue('email')
    scrape = Queue('scrape')
    categorize = Queue('categorize')
    yield SimpleWorker([email, scrape, categorize])


@pytest.yield_fixture()
def outbox(request):
    with mail.record_messages() as outbox:
        yield outbox
