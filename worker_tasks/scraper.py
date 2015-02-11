
from sourcemash.database import db

from sourcemash.models import Item, Feed
from datetime import datetime
from time import mktime
from collections import Counter

from readability.readability import Document
import requests
import feedparser

import logging


class Scraper:

    def __init__(self):
        self.title_categories = Counter()


    def reset_title_categories(self):
        self.title_categories.clear()

        titles = [item.title for item in Item.query.filter_by(category_1=None).all()]
        self.parse_title_categories(titles)


    def parse_title_categories(self, titles):
        for title in titles:
            self.title_categories.update(title.lower().split())


    def get_full_text(self, url):
        html = requests.get(url).content
        return Document(html).summary()


    def store_items_and_category_counts(self, feed):
        logging.info("Starting to parse: %s" % feed.title)

        fp = feedparser.parse(feed.url)
        for item in fp.entries:
            item_last_updated = datetime(*item.updated_parsed[:6])

            # Store counts of categories in article titles
            # Due to concurrency issues, parse all titles
            # even if feed is out of date
            self.parse_title_categories([item.title])

            # Stop when older items hit
            if item_last_updated < feed.last_updated:
                break

            text = self.get_full_text(item.link)

            new_entry = Item(title=item.title, text=text, link=item.link, 
                                last_updated=item_last_updated, author=item.author,
                                summary=item.summary, feed_id=feed.id)

            db.session.add(new_entry)
            db.session.commit()

        feed.last_updated = datetime.utcnow()
        db.session.commit()

        logging.info("Finished parsing: %s" % feed.title)


    def scrape_articles(self):
        # Pull down all articles from RSS feeds
        for feed in Feed.query.all():
            self.store_items_and_category_counts(feed)

        # TODO: Assign categories to articles


