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
from sourcemash.models import User, Feed, Item, Category, UserItem, UserFeed, UserCategory

from worker import create_worker
from worker.categorize import Categorizer
from worker.scraper import scrape_feed_articles, categorize_feed_articles

from datetime import datetime, timedelta
import json

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
conn = create_worker()

manager = Manager(app)
categorizer = Categorizer()

TEST_CMD = "sh ./scripts/test.sh"
FUNCTIONAL_TEST_CMD = "sh ./scripts/functional_test.sh"
FEED_DATA_FILE = "./json/feeds.json"

THIRTY_MINUTES = 30 * 60


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db, 'User': User, 'Item': Item,
            'Category': Category, 'Feed': Feed, 'UserItem': UserItem,
            'UserFeed': UserFeed, 'UserCategory': UserCategory}


@manager.command
def test(all=False):
    """Run the tests. Use -a or --all for functional tests."""
    status = subprocess.call(TEST_CMD, shell=True)

    if all:
        status = subprocess.call(FUNCTIONAL_TEST_CMD, shell=True)

    sys.exit(status)


@manager.command
def scrape():
    """Runs one live scrape of all feeds."""

    for feed in Feed.query.all():
        scrape_feed_articles(feed.id)
        categorize_feed_articles(feed.id, categorizer)


@manager.command
def scrape_loop():
    """Start an infinte loop to scrape & categorize articles."""

    q = Queue('scrape', connection=conn)
    while True:

        for feed in Feed.query.all():
            q.enqueue_call(func=scrape_feed_articles,
                           args=(feed.id,), timeout=1800)

        for feed in Feed.query.all():
            q.enqueue_call(func=categorize_feed_articles,
                           args=(feed.id, categorizer,), timeout=1800)

        too_old = datetime.today() - timedelta(days=30)

        for item in Item.query.filter(Item.last_updated <= too_old).all():

            # Don't delete items recently updated by a user
            recent_user_item = UserItem.query.filter(UserItem.item==item,
                                        UserItem.last_modified > too_old).first()
            if not recent_user_item:
                for user_item in UserItem.query.filter(UserItem.item==item).all():
                    db.session.delete(user_item)
                    db.session.commit()

                db.session.delete(item)
                db.session.commit()

        time.sleep(THIRTY_MINUTES)

@manager.command
def scrape_worker(kill=False):
    """Starts redis queue worker. Requires redis-server"""
    """To run (in background): 'redis-server &'
       To kill: 'redis-cli shutdown' """
    listen = ['scrape', 'email', 'categorize']

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def scrape_worker(kill=False):
    """Starts redis queue worker. Requires redis-server"""
    """To run (in background): 'redis-server &'
       To kill: 'redis-cli shutdown' """
    listen = ['scrape']

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def user_tasks_worker(kill=False):
    """Starts redis queue worker. Requires redis-server"""
    """To run (in background): 'redis-server &'
       To kill: 'redis-cli shutdown' """
    listen = ['email', 'categorize']

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

                feed = Feed.query.filter(Feed.url == feed_json["url"]).first()

                # Don't re-add existing feed
                if not feed:
                    feed = Feed(title=feed_json["title"],
                                url=feed_json["url"],
                                image_url=feed_json["image_url"],
                                topic=topic_json.keys()[0],
                                last_updated=datetime.min,
                                public=True)

                    db.session.add(feed)
                    db.session.commit()

        for feed in Feed.query.all():
            scrape_feed_articles(feed.id)
            categorize_feed_articles(feed.id, categorizer)


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
    scrape_feed_articles(feed.id)
    categorize_feed_articles(feed.id, categorizer)

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets)

if __name__ == '__main__':
    manager.run()
