import logging
import os

basedir = os.path.abspath(os.path.dirname('run.py'))

TESTING = True
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = ('sqlite:///:memory:')
WTF_CSRF_ENABLED = False

BASE_URL = "http://peaceful-falls-6831.herokuapp.com"

SECRET_KEY = os.environ['SECRET_KEY']
WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']

SAUCE_USERNAME = os.environ['SAUCE_USERNAME']
SAUCE_ACCESS_KEY = os.environ['SAUCE_ACCESS_KEY']

logging.info("Travis settings loaded.")