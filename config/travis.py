import logging
import os

TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
CSRF_ENABLED = False

SECRET_KEY = os.environ['SECRET_KEY']
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']

logging.info("Travis settings loaded.")