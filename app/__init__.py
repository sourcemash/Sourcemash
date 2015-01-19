import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('instance.default')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)

from app.frontend import dashboards
from app.api import feeds, users, subscriptions

from app import models