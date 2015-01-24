import os
import logging

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname('run.py'))

CSRF_ENABLED = True
CSRF_SESSION_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_IMPORTS = ("worker_tasks.feed_scraper")

CELERYBEAT_SCHEDULE = {
	'feed-scraper': {
		'task': 'worker_tasks.feed_scraper.ingest_feeds',
		'schedule': crontab(minute="*/1"),
		'args': ()
	}
}

logging.basicConfig(level=logging.DEBUG)

logging.info("Default settings loaded.")