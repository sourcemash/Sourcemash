import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

logging.basicConfig(level=logging.DEBUG)

logging.info("Default settings loaded.")
