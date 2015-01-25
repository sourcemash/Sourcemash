import logging

TESTING = True
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
WTF_CSRF_ENABLED = False

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = None

logging.info("Testing settings loaded.")