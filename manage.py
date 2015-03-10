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
from sourcemash.models import User, Feed, Item, UserItem

from worker_tasks.categorize import Categorizer
from worker_tasks.scraper import scrape_articles

from datetime import datetime

import logging

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)

TEST_CMD = "py.test --cov-report term-missing --cov-config .coveragerc --cov . \
                    --boxed -n14 -k 'not functional' tests/"
FUNCTIONAL_TEST_CMD = "./functional_test.sh"

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db, 'User': User, 'Item': Item, 'Feed': Feed, 'UserItem': UserItem}


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
    categorizer = Categorizer()

    while True:
        logging.info("Starting scrape...")

        scrape_articles(categorizer)

        logging.info("Finished scrape. Let's run it back...")

@manager.command
def seed():
    """Add seed data to the database"""
    """Required: Need to delete database & run db upgrade first"""
    # One user
    user = User(email="admin@sourcemash.com", password="password", active=True)
    db.session.add(user)
    db.session.commit()

    techcrunch = Feed(title='TechCrunch > Startups', 
                url="http://feeds.feedburner.com/techcrunch/startups?format=xml",
                last_updated = datetime.min)
    db.session.add(techcrunch)
    db.session.commit()

    engadget = Feed(title='Engadget', 
            url="http://podcasts.engadget.com/rss.xml",
            last_updated = datetime.min)
    db.session.add(engadget)
    db.session.commit()

    gizmodo = Feed(title='Gizmodo', 
            url="http://feeds.gawker.com/gizmodo/full",
            last_updated = datetime.min)
    db.session.add(gizmodo)
    db.session.commit()

    tnw = Feed(title='The Next Web', 
            url="http://thenextweb.com/feed/",
            last_updated = datetime.min)
    db.session.add(tnw)
    db.session.commit()

    feeds = [techcrunch, engadget, gizmodo, tnw]

    # Subscribe user to feed
    for feed in feeds:
        user.subscribed.append(feed)
        db.session.commit()

    # Scrape articles for feed
    scrape_articles(Categorizer())

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets)

if __name__ == '__main__':
    manager.run()