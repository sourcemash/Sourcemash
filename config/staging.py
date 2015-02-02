import os
import sys
import logging

DEBUG = True

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']
WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

logging.basicConfig(level=logging.DEBUG, streak=sys.stdout)

logging.info("Staging settings loaded.")