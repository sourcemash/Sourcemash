import os

from flask import Flask

app = Flask(__name__)

from app.frontend import dashboards
from app.api import feeds, users, subscriptions

# Logging
if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('rss-aggregator startup')