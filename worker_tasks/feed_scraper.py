from app import db, celery

from app.models import Item, Feed
from datetime import datetime
from time import mktime

import feedparser

@celery.task
def store_items(feed_id, last_updated, feed_url):
	feed = feedparser.parse(feed_url)
	for item in feed.entries:
		update_dt = datetime(*item.updated_parsed[:6])

		# Stop when older items hit
		if update_dt < last_updated:
			break

		new_entry = Item(title=item.title, link=item.link, 
							last_updated=update_dt, author=item.author,
							summary=item.summary, feed_id=feed_id)

		db.session.add(new_entry)
		db.session.commit()

	feed = Feed.query.get(feed_id)
	feed.last_updated = datetime.utcnow()
	db.session.commit()

@celery.task
def ingest_feeds():
	for feed in Feed.query.all():
		store_items.delay(feed.id, feed.last_updated, feed.url)