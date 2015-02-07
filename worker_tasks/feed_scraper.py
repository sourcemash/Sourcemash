
from celery import Celery
from sourcemash import create_app
from sourcemash.database import db

from sourcemash.models import Item, Feed
from datetime import datetime
from time import mktime

from readability.readability import Document
import requests
import feedparser

import logging

app = create_app()

# Celery Task Queue
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


def get_full_text(url):
    html = requests.get(url).content
    return Document(html).summary()


@celery.task
def store_items(feed):
    logging.info("Starting to parse: %s" % feed.title)

    fp = feedparser.parse(feed.url)
    for item in fp.entries:
        item_last_updated = datetime(*item.updated_parsed[:6])

        # Stop when older items hit
        if item_last_updated < feed.last_updated:
            break

        text = get_full_text(item.link)

        new_entry = Item(title=item.title, text=text, link=item.link, 
                            last_updated=item_last_updated, author=item.author,
                            summary=item.summary, feed_id=feed.id)

        db.session.add(new_entry)
        db.session.commit()

    feed.last_updated = datetime.utcnow()
    db.session.commit()

    logging.info("Finished parsing: %s" % feed.title)

@celery.task
def ingest_feeds():
    for feed in Feed.query.all():
        store_items.delay(feed)