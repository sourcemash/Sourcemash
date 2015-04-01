import pytest
import atexit
import os
import sys

from selenium import webdriver
from browser import Browser
from sauceclient import SauceClient


browsers = [{"platform": "Mac OS X 10.9",
             "browserName": "chrome",
             "version": "31"},
            {"platform": "Windows 8.1",
             "browserName": "internet explorer",
             "version": "11"}]


def set_absolute_file_path(*path):
    """Sets the path based on the location of the file."""
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)

@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    # execute all other hooks to obtain the report object
    rep = __multicall__.execute()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)
    return rep

class global_config():
    pass

@pytest.yield_fixture(params=browsers)
def driver(request):

    sauce_username = os.getenv("SAUCE_USERNAME")
    sauce_access_key = os.getenv("SAUCE_ACCESS_KEY")

    if sauce_username and sauce_access_key:
        desired_capabilities = request.param
        desired_capabilities['name'] = "%s.%s_%d" % (request.cls.__name__, request.function.__name__, browsers.index(request.param)+1)

        if os.environ.get('TRAVIS_BUILD_NUMBER'):
            desired_capabilities[
                'build'] = os.environ.get('TRAVIS_BUILD_NUMBER')
            desired_capabilities[
                'tunnel-identifier'] = os.environ.get('TRAVIS_JOB_NUMBER')

        driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor='http://%s:%s@ondemand.saucelabs.com/wd/hub' % (global_confg.sauce_username, global_config.sauce_access_key)
        )

    else:
        driver = webdriver.Firefox()

    driver.maximize_window()

    print "entering function scope driver"
    request.instance.browser = Browser(driver, os.getenv("BASE_URL", "http://localhost:5000"), 10)

    yield request.instance.browser

    if sauce_access_key:
        sauce = SauceClient(sauce_username, sauce_access_key)

    # Update job statuses on completion
    # Save image if local
    if request.node.rep_setup.failed:
        if sauce_access_key:
            sauce.jobs.update_job(driver.session_id, passed=False)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            if sauce_access_key:
                sauce.jobs.update_job(driver.session_id, passed=False)
            else:
                request.instance.browser.driver.get_screenshot_as_file("/tmp/" +
                        str(request.node.nodeid).replace("::", "-").replace("(", '-').replace(")", '-').replace(
                        "tests/", "").replace('/', '-') + ".png")
        if request.node.rep_call.passed and sauce_access_key:
            sauce.jobs.update_job(driver.session_id, passed=False)

    driver.quit()

# @atexit.register
# def erase_cookies_after_all_tests():
#     print "cleaning up temp"
#     files = os.listdir(set_absolute_file_path('temp'))
#     for file_name in files:
#         if file_name.startswith('cookie'):
#              os.remove(set_absolute_file_path('temp', file_name))
