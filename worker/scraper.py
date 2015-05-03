from sourcemash.database import db

from sourcemash.models import Item, Feed
from categorize import Categorizer

from datetime import datetime

from readability.readability import Document
import requests
from urlparse import urlparse
from bs4 import BeautifulSoup
import feedparser

import logging

logger = logging.getLogger('Sourcemash')


def scrape_and_categorize_articles():
    categorizer = Categorizer()

    # Pull down all articles from RSS feeds
    for feed in Feed.query.all():
        _store_items(feed)

    # Assign categories and extract first image from articles
    for item in Item.query.filter_by(categorized=False).all():
        soup = BeautifulSoup(item.text)

        # Extract first image from item
        try:
            img_url = soup.find('img')['src']
            item.image_url = _get_absolute_url(item.feed.url, img_url)
            db.session.commit()
        except:
            pass

        # Extract text and categorize item
        text_only = soup.get_text()
        categories = categorizer.categorize_item(item.title, text_only)
        for category in categories:
            item.categories.append(category)

        item.categorized = True

        db.session.commit()

        logger.info("CATEGORIZED [%s]: %s" % (item.title, item.categories))


def scrape_feed_articles(feed):
    _store_items(feed)

    for item in Item.query.filter_by(feed_id=feed.id).all():
        soup = BeautifulSoup(item.text)

        # Extract first image from item
        try:
            img_url = soup.find('img')['src']
            item.image_url = _get_absolute_image_link(item.feed.url, img_url)
            db.session.commit()
        except:
            pass


def _get_full_text(url):
    html = requests.get(url).content
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
    return Document(html, url=base_url).summary(html_partial=True)

def _get_absolute_url(feed_url, img_url):
    if not "http" in img_url:
        base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(feed_url))

        print "\n\n\n\n\n\n", base_url + url, "\n\n\n\n\n\n\n--------------"
        a = raw_input()
        return base_url + img_url

    return url

def _store_items(feed):
    logger.info("Starting to parse: %s" % feed.title)

    fp = feedparser.parse(feed.url)
    for item in fp.entries:
        try:
            item_last_updated = datetime(*item.updated_parsed[:6])
        except:
            try:
                item_last_updated = datetime(*item.published_parsed[:6])
            except:
                item_last_updated = datetime.utcnow()

        if item_last_updated < feed.last_updated:
            continue

        text = _get_full_text(item.link)

        new_entry = Item(title=item.title, text=text, link=item.link,
                            last_updated=item_last_updated, author=getattr(item, 'author', None),
                            summary=getattr(item, 'summary', None), feed_id=feed.id)

        db.session.add(new_entry)
        db.session.commit()

    if not feed.image_url:
        try:
            feed.image_url = fp.feed.image.url
            db.session.commit()
        except:
            try:
                img_tags = BeautifulSoup(requests.get(fp.feed.link).content).find_all('img')
                for image_tag in img_tags:
                    if "logo" in str(image_tag):
                        image_url = image_tag.get('src') or image_tag.get('href')
                        feed.image_url = _get_absolute_url(image_url)
                        db.session.commit()
                        break
            except:
                pass

    if not feed.description:
        try:
            feed.description = fp.feed.description
        except:
            feed.description = "Recent news from " + feed.title + "."

    try:
        feed.last_updated = datetime(feed.updated_parsed[:6])
    except:
        feed.last_updated = datetime.utcnow()

    db.session.commit()

    logger.info("Finished parsing: %s" % feed.title)
