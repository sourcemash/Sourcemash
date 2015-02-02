#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from app import create_app
from app.database import db
from app.users.models import User

app = create_app(os.environ.get("APP_CONFIG_FILE") or "development")
manager = Manager(app)

TEST_CMD = "py.test --boxed -n10 -k 'not functional' tests/"
FUNCTIONAL_TEST_CMD = "./functional_test.sh"

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


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print "To run Celery:"
    print "  redis-server --daemonize yes"
    print "  celery -A worker_tasks.feed_scraper worker --loglevel=debug --beat"
    manager.run()