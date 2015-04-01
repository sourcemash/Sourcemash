# Adapted from Smohapatra/Sailthru-magento

from itertools import count
import datetime
import pytz
import random
import os

class BasePage(object):
    """This class will be inherited by all page objects. Provides common
    functions to all page objects and global navigation methods."""

    def __init__(self, browser):
        self.browser = browser

    prior_page = None
    counter = count(10)

    @classmethod
    def set_absolute_file_path(cls, *path):
        """Sets the path based on the location of the file."""
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)

    @classmethod
    def format_locator(cls, locator_tuple, string):
        """Formats the locator in a locator tuple"""
        by, locator, description = locator_tuple
        return by, locator.format(string), description

    @classmethod
    def update_prior_page(cls, page):
        cls.prior_page = page

    @classmethod
    def get_next_integer(cls):
        """Returns the next integer from an infinite counter as a string. Starts at 10."""
        return str(next(cls.counter))

    @classmethod
    def get_random_integer(cls, digits = 5):
        """Returns a random integer, default is a 5 digit number."""
        return int(random.random * (10 ** digits))

    @classmethod
    def get_todays_date(cls):
        return datetime.date.today().strftime("%m/%d/%Y")

    @classmethod
    def get_timestamp(cls):
        """Returns current timestamp including fraction of a second (%f)"""
        return datetime.datetime.now().strftime("%Y%m%d%H%M%f")

    @classmethod
    def get_current_datetime(cls):
        fmt = '%Y%m%d%H%M%S'
        d = datetime.datetime.now(pytz.timezone("America/New_York"))
        d_string = d.strftime(fmt)
        d2 = datetime.datetime.strptime(d_string, fmt)
        return d2.strftime(fmt)

    # run scrit
    #$("#f_source_list option").attr('selected', null)
    #$("#f_source_list option[value='10 users']").attr('selected', 'selected');
    def set_option_for_javascript_dropdown(self, locator, option):
        self.browser.execute_script("$('{0} option').attr('selected', null);".format(locator))
        self.browser.execute_script("$('{0} option[value=\"{1}\"]').attr('selected', 'selected')".format(locator, option))
