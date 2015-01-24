import logging

TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
CSRF_ENABLED = False

CELERY_BROKER_URL = 'memory://'
CELERY_RESULT_BACKEND = None

logging.info("Testing settings loaded.")