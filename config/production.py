import os
import logging

DEBUG = False
SQLALCHEMY_ECHO = False

SECURITY_CONFIRMABLE = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = os.environ['SECRET_KEY']

logger = logging.getLogger('Sourcemash')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

logger.info("Production settings loaded.")
