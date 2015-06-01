from sourcemash.database import db

from sourcemash.models import Item, Feed, Category, UserFeed, UserCategory

from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound
from readability.readability import Document
import requests
from urlparse import urlparse
from bs4 import BeautifulSoup
import feedparser

import logging

logger = logging.getLogger('Sourcemash')

SOURCEMASH_LOGO_URL = "http://sourcemash.com/static/img/solologo.svg"


def scrape_feed_articles(feed):
    _store_items(feed)

    for item in Item.query.filter_by(feed_id=feed.id).all():

        # Extract first image from item
        try:
            summary_soup = BeautifulSoup(item.summary)
            img_url = summary_soup.find('img', width_=lambda x: x != 1)['src']
            item.image_url = _get_absolute_url(item.link, img_url)
            db.session.commit()
        except:
            try:
                soup = BeautifulSoup(item.text)
                img_url = soup.find('img')['src']
                item.image_url = _get_absolute_url(item.link, img_url)
                db.session.commit()
            except:
                item.image_url = SOURCEMASH_LOGO_URL
                db.session.commit()


def categorize_feed_articles(feed, categorizer):
    for item in Item.query.filter_by(categorized=False).all():
        soup = BeautifulSoup(item.text)

        # Extract text and categorize item
        text_only = soup.get_text()
        categories = categorizer.categorize_item(item.title, text_only)
        for category in categories:
            if category in item.categories:
                continue

            item.categories.append(category)

            # Mark category as unread for all users
            try:
                category_model = Category.query.filter_by(category=category).one()
                UserCategory.query.filter_by(category=category_model).update({"unread": True})
                db.session.commit()
            except NoResultFound:
                pass

        item.categorized = True

        db.session.commit()

        logger.info("CATEGORIZED [%s]: %s" % (item.title, item.categories))


def categorize_article_by_url(url, categorizer):
    html = requests.get(url).text
    full_page = BeautifulSoup(html)
    full_text = BeautifulSoup(Document(html).summary())
    title = full_page.title.string if full_page.title else ""
    categories = categorizer.categorize_item(title, full_text.get_text())
    return [{'name': cat} for cat in categories]


def _get_full_text(url):
    html = requests.get(url).content
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
    return Document(html, url=base_url).summary(html_partial=True)


def _get_absolute_url(base_url, img_url):
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(base_url))

    # If img_url is already an absolute url
    # (i.e. contains .com or http)
    if base_url.split('.')[-1] in img_url or "http" in img_url:
        return img_url

    return base_url + img_url


def _store_items(feed):
    logger.info("Starting to parse: %s" % feed.title)

    fp = feedparser.parse(feed.url)

    feed.item_count = Feed.query.get(feed.id).items.count()
    new_item_count = 0

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

        new_item_count += 1

    feed.item_count += new_item_count
    db.session.commit()

    # Mark feed as unread for all users
    if new_item_count > 0:
        UserFeed.query.filter_by(feed_id=feed.id).update({"unread": True})
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
                        feed.image_url = _get_absolute_url(fp.feed.link, image_url)
                        db.session.commit()
                        break
            except:
                pass

        if not feed.image_url:
            feed.image_url = SOURCEMASH_LOGO_URL
            db.session.commit()

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
