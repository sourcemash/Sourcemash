import os
import sys
import logging

DEBUG = True
SQLALCHEMY_ECHO = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']

logger = logging.getLogger('Sourcemash')
logger.setLevel(logging.DEBUG)
logger.addHandler(sys.stdout)

logger.info("Staging settings loaded.")