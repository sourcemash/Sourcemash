from sourcemash.database import db

from sourcemash.models import Item, Feed
from datetime import datetime
from string import punctuation
from collections import Counter

from readability.readability import Document
import requests
import feedparser

import logging

def scrape_articles(categorizer):
    # Pull down all articles from RSS feeds
    for feed in Feed.query.all():
        _store_items_and_category_counts(feed, categorizer)

    # Assign categories to articles after all feeds are processed
    for item in Item.query.filter_by(category_1=None).all():
        item.category_1, item.category_2 = categorizer.categorize_item(item.title, item.text)
        db.session.commit()
        logging.info("CATEGORIZED [%s]: (%s, %s)" % (item.title, item.category_1, item.category_2))


def _get_full_text(url):
    html = requests.get(url).content
    return Document(html).summary()


def _store_items_and_category_counts(feed, categorizer):
    logging.info("Starting to parse: %s" % feed.title)

    fp = feedparser.parse(feed.url)
    for item in fp.entries:
        item_last_updated = datetime(*item.updated_parsed[:6])

        # Store counts of categories in article titles
        # Due to concurrency issues, parse all titles
        # even if feed is out of date
        categorizer.parse_title_categories([item.title])

        # Stop when older items hit
        if item_last_updated < feed.last_updated:
            break

        text = _get_full_text(item.link)

        new_entry = Item(title=item.title, text=text, link=item.link, 
                            last_updated=item_last_updated, author=getattr(item, 'author', None),
                            summary=getattr(item, 'summary', None), feed_id=feed.id)

        db.session.add(new_entry)
        db.session.commit()

    feed.last_updated = datetime.utcnow()
    db.session.commit()

    logging.info("Finished parsing: %s" % feed.title)