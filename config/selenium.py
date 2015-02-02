import os
import logging

basedir = os.path.abspath(os.path.dirname('run.py'))

TESTING = True
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'test.db'))
WTF_CSRF_ENABLED = False

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = None

logging.info("Functional testing settings loaded.")