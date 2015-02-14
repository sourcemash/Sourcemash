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
from sourcemash.users.models import User
from worker_tasks.scraper import scrape_articles, reset_title_categories

import logging

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)

TEST_CMD = "py.test --boxed -n10 -k 'not functional' tests/"
FUNCTIONAL_TEST_CMD = "./functional_test.sh"

CATEGORY_DICT_LIFETIME = 2      # days
SCRAPE_INTERVAL = 1200          # seconds
SECONDS_PER_DAY = 86400
ITERATIONS_BEFORE_RESET = CATEGORY_DICT_LIFETIME * SECONDS_PER_DAY / SCRAPE_INTERVAL

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default."""
    return {'app': app, 'db': db, 'User': User}


@manager.command
def test(all=False):
    """Run the tests. Use -a or --all for functional tests."""
    status = subprocess.call(TEST_CMD, shell=True)

    if all:
        status = subprocess.call(FUNCTIONAL_TEST_CMD, shell=True)
    
    sys.exit(status)


@manager.command
def scrape():
    """Start an infinte loop to scrape articles."""
    iterations = 0

    while True:
        logging.info("Starting scrape...")
        if (iterations % ITERATIONS_BEFORE_RESET) == 0:
            reset_title_categories()

        scrape_articles()

        iterations += 1
        logging.info("Finished scrape. Zzz...")
        time.sleep(SCRAPE_INTERVAL)


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("assets", ManageAssets)

if __name__ == '__main__':
    manager.run()