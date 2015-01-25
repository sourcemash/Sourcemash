import os
import sys
import logging

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']

CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']

logging.basicConfig(level=logging.INFO, streak=sys.stdout)

logging.info("Production settings loaded.")