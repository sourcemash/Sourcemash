import os
import logging

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']
CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']

logging.basicConfig(level=logging.INFO, streak=sys.stdout)

logging.info("Production settings loaded.")