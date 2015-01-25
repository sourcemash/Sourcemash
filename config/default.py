import os
import logging

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname('run.py'))

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_IMPORTS = ("worker_tasks.feed_scraper")

CELERYBEAT_SCHEDULE = {
    'feed-scraper': {
        'task': 'worker_tasks.feed_scraper.ingest_feeds',
        'schedule': crontab(minute="0,20,40"),
        'args': ()
    }
}

# Flask security config variables- https://pythonhosted.org/Flask-Security/configuration.html
SECURITY_FLASH_MESSAGES = True
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "abcde1234509876zyxwvu22"
SECURITY_POST_LOGIN_VIEW = "/profile"
SECURITY_POST_LOGOUT_VIEW = "/login"
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

SECURITY_MSG_INVALID_PASSWORD = ("Invalid username/password combination", "error")
SECURITY_MSG_PASSWORD_NOT_PROVIDED = ("Invalid username/password combination", "error")
SECURITY_MSG_USER_DOES_NOT_EXIST = ("Invalid username/password combination", "error")

logging.basicConfig(level=logging.DEBUG)

logging.info("Default settings loaded.")
