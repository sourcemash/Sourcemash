import os
import sys
import pytest

from sqlalchemy.orm import Session, scoped_session, sessionmaker
from app import create_app
from app.database import db as _db
from tests.factories import feed_factories, item_factories, role_factories, user_factories

from selenium import webdriver
from sauceclient import SauceClient

browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": "31"},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"}]

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
    feed_factories.NYTFeedFactory._meta.sqlalchemy_session = session
    user_factories.UserFactory._meta.sqlalchemy_session = session
    item_factories.ItemFactory._meta.sqlalchemy_session = session
    role_factories.RoleFactory._meta.sqlalchemy_session = session

    yield db.session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.yield_fixture()
def test_client(app, request):
    with app.test_client() as client:
        yield client

@pytest.yield_fixture(params=browsers)
def driver(app, request):

    sauce = SauceClient(app.config["SAUCE_USERNAME"], app.config["SAUCE_ACCESS_KEY"])

    desired_capabilities = request.param
    desired_capabilities['name'] = "%s.%s_%d" % (request.cls.__name__, request.function.__name__, browsers.index(request.param)+1)
    desired_capabilities['username'] = app.config["SAUCE_USERNAME"]
    desired_capabilities['access-key'] = app.config["SAUCE_ACCESS_KEY"]

    if os.environ.get('TRAVIS_BUILD_NUMBER'):
        desired_capabilities[
            'build'] = os.environ.get('TRAVIS_BUILD_NUMBER')
        desired_capabilities[
            'tunnel-identifier'] = os.environ.get('TRAVIS_JOB_NUMBER')

    driver = webdriver.Remote(
        desired_capabilities=desired_capabilities,
        command_executor='http://%s:%s@ondemand.saucelabs.com/wd/hub' % (app.config["SAUCE_USERNAME"], app.config["SAUCE_ACCESS_KEY"])
    )
    driver.implicitly_wait(30)

    yield driver

    try:
        if sys.exc_info() == (None, None, None):
            sauce.jobs.update_job(
                driver.session_id, passed=True, public=True)
        else:
            sauce.jobs.update_job(
                driver.session_id, passed=False, public=True)
    finally:
        driver.quit()