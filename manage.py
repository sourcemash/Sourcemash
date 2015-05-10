#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.assets import ManageAssets
from rq import Worker, Queue, Connection

from sourcemash import create_app
from sourcemash.database import db
from sourcemash.models import User, Feed, Item, Category, UserItem

from worker import create_worker
from worker.scraper import scrape_and_categorize_articles

from datetime import datetime
import json

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
conn = create_worker(os.environ.get("APP_CONFIG_FILE") or "development")

manager = Manager(app)

TEST_CMD = "sh ./scripts/test.sh"
FUNCTIONAL_TEST_CMD = "sh ./scripts/functional_test.sh"
FEED_DATA_FILE = "./json/feeds.json"

THIRTY_MINUTES = 30 * 60


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db, 'User': User, 'Item': Item,
            'Category': Category, 'Feed': Feed, 'UserItem': UserItem}


@manager.command
def test(all=False):
    """Run the tests. Use -a or --all for functional tests."""
    status = subprocess.call(TEST_CMD, shell=True)

    if all:
        status = subprocess.call(FUNCTIONAL_TEST_CMD, shell=True)

    sys.exit(status)


@manager.command
def scrape(noqueue=False):
    """Start an infinte loop to scrape & categorize articles."""

<<<<<<< HEAD
    if noqueue:
        scrape_and_categorize_articles()
    else:
        q = Queue('default', connection=conn)
        while True:
            job = q.enqueue_call(func=scrape_and_categorize_articles, timeout=1800)
            time.sleep(THIRTY_MINUTES)

=======
    q = Queue('default', connection=conn)
    while True:
        q.enqueue_call(func=scrape_and_categorize_articles, timeout=1800)
        time.sleep(THIRTY_MINUTES)
>>>>>>> PR fixes.


@manager.command
def worker(kill=False):
    """Starts redis queue worker. Requires redis-server"""
    """To run (in background): 'redis-server &'
       To kill: 'redis-cli shutdown' """
    listen = ['default']

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def feed_seed():
    """Add seed feeds from JSON file"""
    with open(FEED_DATA_FILE) as data_file:
        data = json.load(data_file)
        feeds_by_topic = data["feeds"]

        for topic_json in feeds_by_topic:
            for feed_json in topic_json.values()[0]:

                # Don't re-add existing feed
                if not Feed.query.filter_by(url=feed_json["url"]).first():

                    feed = Feed(title=feed_json["title"],
                                url=feed_json["url"],
                                image_url=feed_json["image_url"],
                                topic=topic_json.keys()[0],
                                last_updated = datetime.min,
                                public=True)

                    db.session.add(feed)
                    db.session.commit()

    # Scrape articles for feed
    scrape_and_categorize_articles()


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
                      topic="Technology",
                      last_updated=datetime.min,
                      public=True)
    db.session.add(techcrunch)
    db.session.commit()

    engadget = Feed(title='Engadget',
                    url="http://www.engadget.com/rss-full.xml",
                    topic="Technology",
                    last_updated=datetime.min,
                    public=True)
    db.session.add(engadget)
    db.session.commit()

    gizmodo = Feed(title='Gizmodo',
                   url="http://feeds.gawker.com/gizmodo/full",
                   topic="Technology",
                   last_updated=datetime.min,
                   public=True)
    db.session.add(gizmodo)
    db.session.commit()

    tnw = Feed(title='The Next Web',
               url="http://thenextweb.com/feed/",
               topic="Technology",
               last_updated=datetime.min,
               public=True)
    db.session.add(tnw)
    db.session.commit()

    feeds = [techcrunch, engadget, gizmodo, tnw]

    # Subscribe user to feed
    for feed in feeds:
        user.subscribed.append(feed)
        db.session.commit()

    # Scrape articles for feed
    scrape_and_categorize_articles()

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets)

if __name__ == '__main__':
    manager.run()
