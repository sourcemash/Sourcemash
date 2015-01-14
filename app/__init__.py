from flask import Flask
import os

app = Flask(__name__)
from app import views

# Logging
if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('rss-aggregator startup')