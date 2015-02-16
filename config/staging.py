import os
import sys
import logging

DEBUG = True
SQLALCHEMY_ECHO = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']

logging.basicConfig(level=logging.DEBUG, streak=sys.stdout)

logging.info("Staging settings loaded.")