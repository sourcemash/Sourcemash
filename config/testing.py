import os
import logging

basedir = os.path.abspath(os.path.dirname('run.py'))

TESTING = True
LOGIN_DISABLED = False
SQLALCHEMY_DATABASE_URI = ('sqlite:///:memory:')
WTF_CSRF_ENABLED = False

logging.info("Testing settings loaded.")