import logging

TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
CSRF_ENABLED = False

logging.info("Testing settings loaded.")