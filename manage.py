#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets

from sourcemash import create_app
from sourcemash.database import db
from sourcemash.models import User, Feed
from sourcemash.categorize import Categorizer
from worker_tasks.scraper import scrape_articles

from datetime import datetime

import logging

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)

TEST_CMD = "py.test --cov-config .coveragerc --cov sourcemash \
                    --boxed -n10 -k 'not functional' tests/"
FUNCTIONAL_TEST_CMD = "./functional_test.sh"

CATEGORY_DICT_LIFETIME = 2      # days
SCRAPE_INTERVAL = 1200          # seconds
SECONDS_PER_DAY = 86400
ITERATIONS_BEFORE_RESET = CATEGORY_DICT_LIFETIME * SECONDS_PER_DAY / SCRAPE_INTERVAL

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test(all=False):
    """Run the tests. Use -a or --all for functional tests."""
    status = subprocess.call(TEST_CMD, shell=True)

    if all:
        status = subprocess.call(FUNCTIONAL_TEST_CMD, shell=True)
    
    sys.exit(status)


@manager.command
def scrape():
    """Start an infinte loop to scrape & categorize articles."""
    iterations = 0
    categorizer = Categorizer()

    while True:
        logging.info("Starting scrape...")
        if (iterations % ITERATIONS_BEFORE_RESET) == 0:
            categorizer.reset_title_categories()

        scrape_articles(categorizer)

        iterations += 1
        logging.info("Finished scrape. Zzz...")
        time.sleep(SCRAPE_INTERVAL)

@manager.command
def seed():
    """Add seed data to the database"""
    """Required: Need to delete database & run db upgrade first"""
    # One user
    user = User(email="admin@sourcemash.com", password="password", active=True)
    db.session.add(user)
    db.session.commit()

    # One feed
    feed = Feed(id=1, title='TechCrunch > Startups', 
                url="http://feeds.feedburner.com/techcrunch/startups?format=xml",
                last_updated = datetime.min)
    db.session.add(feed)
    db.session.commit()

    # Subscribe user to feed
    user.subscribed.append(feed)
    db.session.commit()

    # Add known article to generate known categories
    

    # Scrape articles for feed
    scrape_articles(Categorizer())

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets)

if __name__ == '__main__':
    manager.run()