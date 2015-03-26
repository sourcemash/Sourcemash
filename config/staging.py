import os
import logging

DEBUG = True
SQLALCHEMY_ECHO = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']

logger = logging.getLogger('Sourcemash')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

logger.info("Staging settings loaded.")
