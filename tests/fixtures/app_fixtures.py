import os
import sys
import pytest

from sqlalchemy.orm import Session, scoped_session, sessionmaker
from app import create_app
from app.database import db as _db
from tests.factories import feed_factories, item_factories, role_factories, user_factories


@pytest.yield_fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application"""
    app = create_app()

    # Establish an application context before running the tests.
    ctx = app.test_request_context()
    ctx.push()

    yield app
    
    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app, request):
    """Session-wide test database"""

    _db.create_all()
    _db.app = app

    yield _db

    _db.drop_all()

@pytest.yield_fixture(scope='function', autouse=True)
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    db.session = session

    feed_factories.FeedFactory._meta.sqlalchemy_session = session
    feed_factories.NYTFeedFactory._meta.sqlalchemy_session = session
    user_factories.UserFactory._meta.sqlalchemy_session = session
    item_factories.ItemFactory._meta.sqlalchemy_session = session
    role_factories.RoleFactory._meta.sqlalchemy_session = session

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture(scope='function')
def test_client(app, request):
    with app.test_client() as client:
        yield client