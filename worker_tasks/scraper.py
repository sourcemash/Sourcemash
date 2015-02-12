
from sourcemash.database import db

from sourcemash.models import Item, Feed
from sourcemash.categorize import categorizeItem
from datetime import datetime, timedelta
from time import mktime
from string import punctuation
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

        one_day_ago = datetime.now() - timedelta(hours=24)
        titles = [item.title for item in Item.query.filter(Item.category_1==None, Item.last_updated>=one_day_ago).all()]
        self.parse_title_categories(titles)


    def parse_title_categories(self, titles):
        for title in titles:
            for word in title.split():
                if len(word) > 3: # crude non-important word remover
                    self.title_categories.update([word.strip(punctuation)])


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
                                last_updated=item_last_updated, author=getattr(item, 'author', None),
                                summary=getattr(item, 'summary', None), feed_id=feed.id)

            db.session.add(new_entry)
            db.session.commit()

        feed.last_updated = datetime.utcnow()
        db.session.commit()

        logging.info("Finished parsing: %s" % feed.title)


    def scrape_articles(self):
        # Pull down all articles from RSS feeds
        for feed in Feed.query.all():
            self.store_items_and_category_counts(feed)

        # Assign categories to articles after all feeds are processed
        for item in Item.query.filter_by(category_1=None).all():
            (cat1, cat2) = categorizeItem(item.title, item.text, self.title_categories)
            item.category_1 = cat1
            item.category_2 = cat2
            db.session.commit()
            logging.info("Categorized item %s: %s, %s" % (item.title, item.category_1, item.category_2))
