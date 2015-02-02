# Taken from Smohapatra/Sailthru-magento

import inspect
import time
from urlparse import urljoin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import alert_is_present
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.remote.webelement import WebElement

# Extend WebElement to parse locator elements
def find_element_by_locator(self, locator):
    by, locator, _ = locator
    return self.find_element(by, locator)

def find_elements_by_locator(self, locator):
    by, locator, _ = locator
    return self.find_elements(by, locator)

WebElement.find_element_by_locator = find_element_by_locator
WebElement.find_elements_by_locator = find_elements_by_locator

# def print_stack_trace(f):
#     def wrapper(*args, **kwargs):
#         print '---inspecting get element call, who is the caller--'
#         print inspect.stack()[1]
#         print '-level 2-'
#         print inspect.stack()[2]
#         print '-level 3-'
#         print inspect.stack()[3]
#         print '-level 4-'
#         print inspect.stack()[4]
#         print inspect.getmodule(inspect.stack()[0])
#         print '---end---'
#         return f(*args, **kwargs)
#     return wrapper


class Browser(object): 
    """This is a wrapper to the Selenium Webdriver API. It wraps common functions so that
    it can retrieve elements while automatically handling common issues and also provide
    waiting methods to synchronize the interaction of tests."""
    
    def __init__(self, driver, base_url, timeout):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.scope = 'session'
    
    @property
    def main_domain_url(self) :
        """Returns the main URL in the form of http://domain.com"""
        return self.base_url
    
    @main_domain_url.setter
    def main_domain_url(self, url):
        """Sets the main URL. Format should be prefix://FQDN """
        self.base_url = url

    def quit(self):
        """Closes the browser and releases the webdriver resource."""
        self.driver.quit()
     
    def maximize_window(self):
        """Maximize window to screen width and height."""
        #self.execute_script("window.moveTo(0,0);window.resizeTo(screen.width,screen.height);")
        self.driver.maximize_window()
        
    def go_to(self, url):
        """Navigate to a page."""
        self.driver.get(url)

    def go_to_relative_url(self, relative_url):
        """Navigate to a URL using the predefined base URL."""
        self.driver.get(urljoin(self.main_domain_url, relative_url))
    
    @property    
    def title(self):
        """Get title of web page."""
        return self.driver.title
    
    def navigate_back_a_page(self):
        """Navigate a page back as if the user pressed the browser's back button."""
        self.driver.back()
    
    def navigate_forward(self):
        """Navigate forward in the history, as if the user pressed browser's forward button."""
        self.driver.forward()
     
    def refresh(self):
        """Reloads/refreshes the browser page."""
        self.driver.refresh()
    
    def switch_to_frame(self, frame):
        """Switches to a frame or iframe by id (an int like 0,1,2...)
        or WebElement that is a frame or iframe elemnent
        or frame name ex <frame name='inner'> """
        self.driver.switch_to_frame(frame)
     
    def switch_to_main_frame(self):
       """Switches to the main/top/default frame."""
       self.driver.switch_to_default_content()
    
    def return_active_element(self):
        """Returns the active web element. Similar to document.activeElement' in Javascript.
        If there's no active element it returns the BODY element. """
        return self.driver.switch_to_active_element()
    
    def close_window(self):
        """Closes the current browser window, if there is more than one. For a solo window, use quit()."""
        if len(self.driver.window_handles) > 1:
            self.driver.close()
    
    def get_cookie(self, name):
        """Returns a single cookie by name. Returns a single cookie if found, None if not."""
        return self.driver.get_cookie(name)

    def get_cookies(self):
        """Returns a set of dictionaries, that are cookies for the current session."""
        return self.driver.get_cookies()

    def delete_cookie(self, name):
        """Deletes a single cookie that matches the name."""
        self.driver.delete_cookie(name)
   
    def add_cookie(self, cookie_dict):
        """Adds a cookie to the current session.
        Cookie is a dict with these required keys:
        {'name': 'foo', 'value': 'baz'}
        Optional keys: path, domain, secure, expiry"""
        self.driver.add_cookie(cookie_dict)

    def delete_all_cookies(self):
        """Deletes all cookies in the cookie cache."""
        self.driver.delete_all_cookies()
    
    @property
    def get_page_source(self):
        """Returns a dump of the DOM."""
        return self.driver.page_source
    
    @property
    def get_current_url(self):
        """Returns the current URL listed in the browser."""
        return self.driver.current_url
    
    @property
    def get_current_relative_url(self):
        """Returns current URL listed in the browser without the base URL"""
        url = self.driver.current_url
        return url.replace(self.base_url, "")

    @property
    def get_window_handle(self):
        """Returns the GUID representing the current window handle of the browser."""
        return self.driver.current_window_handle
    
    @property
    def get_window_handles(self):
        """Returns a list of active window handles."""
        return self.driver.window_handles
    
    def switch_to_new_window(self):
        """Switches to a new window, assumes only two windows exist."""
        main_window = self.driver.current_window_handle
        handles = self.driver.window_handles
        for handle in handles:
            if handle != main_window:
                self.driver.switch_to_window(handle)
        # The following is faster to execute, but not a particularly useful optimization
        #main_window = set(self.driver.current_window_handle)
        #handles = set(self.driver.window_handles)
        #self.driver.switch_to_window((handles - mainWindow).pop())
        
    def switch_back_to_main_window(self):
        """Switches back to main window if the other window was just closed."""
        handles = self.driver.window_handles
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(handles[0])
        # perhaps page object keeps track of main window handle

    # @print_stack_trace
    def get_element(self, locator, interval=None, wait_first=False):
        """Attempts to locate an element until the timeout and returns
        a WebElement."""
        return self.get_element_or_elements(locator, False, interval, wait_first)

    def get_elements(self, locator, interval=None, wait_first=False):
        """Attempts to find elements until the timeout and returns a list of
        WebElements. Note the webdriver API allows for 0 elements to be located.
        Use one of the visibility methods for this case."""
        return self.get_element_or_elements(locator, True, interval, wait_first)
    
    def presence_of_at_least_one_element_located_by(self, driver, locator):
        """Expected Condition: Return at least one element"""
        try:
            elements = driver.find_elements(*locator)
            if elements:
                return elements
            else:
                return False
        except StaleElementReferenceException:
            return False

    def presence_of_element_located_by(self, driver, locator):
        """Expected Condition: Return an element"""
        try:
            return driver.find_element(*locator)
        except StaleElementReferenceException:
            return False
        
    def get_element_or_elements(self, locator, plural, interval, wait_first):
        if not interval:
            interval = 0.5
        locator, human_description = locator[0:2], locator[2]
        timeout_in_seconds = self.get_timeout_seconds()
        if wait_first:
            time.sleep(interval)
        if plural:
            return WebDriverWait(self.driver, timeout_in_seconds, interval).until(
                (lambda d: self.presence_of_at_least_one_element_located_by(d, locator)),
                "No elements described as: {0} | located by: {1}".format(human_description, locator))
        else:
            return WebDriverWait(self.driver, timeout_in_seconds, interval).until(
                (lambda d: self.presence_of_element_located_by(d, locator)),
                "No element found described as: {0} | located by: {1}".format(human_description, locator))

    def element_is_not_stale(self, driver, locator):
        """Expected Condition: Get an element and test if it's stale. Useful for other wait functions."""
        try:
            element = driver.find_element(*locator)
            element.is_enabled()
            return element
        except StaleElementReferenceException:
            return False

    def get_stable_element(self, locator):
        locator, human_description = locator[0:2], locator[2]
        return WebDriverWait(self.driver, self.timeout).until(
            (lambda d: self.element_is_not_stale(d, locator)),
            "Element described as {0} is not present or still stale. {1}".format(human_description, locator)
            )

    def _click_element(self, driver, locator):
        """ExpectedCondition: Click on a element until it succeeds. May not be reliable."""
        try:
            driver.find_element(*locator).click()
            return True
        except (StaleElementReferenceException, ElementNotVisibleException):
            return False
         
    def click_element_by(self, locator):
        locator, human_description = locator[0:2], locator[2]
        """Locates and clicks on a element until it succeeds. This function shouldn't be used, but 
        it's a good quick fix until a better wait method is found."""

        timeout_in_seconds = self.get_timeout_seconds()
        WebDriverWait(self.driver, timeout_in_seconds).until(
            (lambda d: self._click_element(d, locator)),
             "Could not locate or click element described as '{0}' located at: {1}".format(human_description, locator))
       
    def is_element_visible(self, element): # or locator
        """Determines if a given WebElement or locator is visible."""
        if isinstance(element, tuple):
            element = element[0:2]
            try:
                element = WebDriverWait(self.driver, 3).until(lambda d: d.find_element(*element))
            except TimeoutException:
                return False
        return element.is_displayed()
  
    def wait_for_element_to_become_visible(self, element, human_description='',
            timeout=None):
        """Waits until the given element or locator becomes visible.
        If waiting on a WebElement provide a description of the element,
        otherwise, locator already contains a description of the element."""
        if not timeout:
            timeout = self.timeout
        if isinstance(element, tuple): # element is a locator tuple
            human_description = element[2]
            WebDriverWait(self.driver, timeout).until(self.locator_is_visible(element[0:2]),
                          "Element located at {0} and described as {1},"
                          " did not become visible.".format(element[0:2], human_description))
        else:
            WebDriverWait(self.driver, self.timeout).until(
                (lambda d: self.element_is_visible(d, element)),
                'Element described as {0} did not become visible.'.format(human_description))

    def wait_for_element_to_become_invisible(self, element,
            human_description='', timeout=None):
        """Waits until the given element is no longer displayed.
         Element still exists in the DOM.
         If waiting on a WebElement provide a description of the element,
         otherwise, locator already contains a description of the element."""
        if not timeout:
            timeout = self.timeout
        if isinstance(element, tuple): # element is a locator tuple
            human_description = element[1]
            element = self.get_element(element)
        WebDriverWait(self.driver, timeout).until_not(
            (lambda d: self.element_is_visible(d, element)),
            'Element described as {0} is still visible.'.format(human_description))

    def element_becomes_stale(self, ignored, element):
        """ExpectedCondition: Returns true if an element is no longer present."""
        try:
            element.is_enabled() # checking an element's state does a staleness check before looking at an attribute
            return False
        except (StaleElementReferenceException, ElementNotVisibleException, NoSuchElementException):
            return True
        
    def wait_for_visible_element_to_disappear(self, element,
            human_description='', timeout=None):
        """Waits for an element or locator to no longer exist in the DOM."""
        if timeout == None:
            timeout = self.timeout
        if isinstance(element, tuple): # element is a locator tuple
            WebDriverWait(self.driver, timeout).until_not(
                    lambda d: self.presence_of_at_least_one_element_located_by(d, element[0:2]),
                    'Element at {0} described as {1} '
                    'is still present.'.format(element[0:2], human_description or element[2]))
            return
        WebDriverWait(self.driver, timeout).until((lambda d: self.element_becomes_stale(d, element)),
                'Element described as {0} is still present'.format(human_description))

    def wait_for_element_to_stop_mutating(self, locator):
        """Waits for an element or locator to stop updating. Experimental"""
        # start = self.now()
        # success = False
        # while (self.now() < start + 3.0):
        #         element = self.get_element(locator)
        #         try:
        #             element.is_enabled()
        #             success = True
        #         except WebDriverException:
        #             success = False
        # if not success:
        #     raise Exception("Element is not present or still mutating after 3 seconds.")
        pass
                         
    def element_is_visible(self, ignored, element):
        """ExpectedCondition: Returns True if element is visible otherwise False"""
        try:
            return element.is_displayed()
        except WebDriverException:
            return False

    class locator_is_visible(object):
        """ExpectedCondition: Waits for element to be visible. Handles condition where the element can go stale."""
        def __init__(self, locator):
            self.locator = locator
        def __call__(self, driver):
            try:
                return driver.find_element(*self.locator).is_displayed()
            except (StaleElementReferenceException):
                return False

    def now(self):
            """Return current time as time since epoch"""
            return time.time()
 
    def get_timeout_seconds(self):
        """Returns the timeout in seconds as defined in the configuration file."""
        return self.timeout
        # CONFIG 'browser.timeout'
    
    def pause(self, seconds):
        """Sleeps for number of seconds specified"""
        try :
            time.sleep(seconds);
        except KeyboardInterrupt:
            raise Exception("Control-C pressed during sleep.")
    
    def does_element_exist(self, locator):
        """Returns True if an element exists in the DOM, False if it does not exist."""
        locator = locator[0:2]
        try :
            WebDriverWait(self.driver, 3).until(lambda d: d.find_element(*locator))
            return True
        except TimeoutException:
            return False
    
    def get_css_property(self, element, css_property):
        """Deprecated"""
        #js = "return document.defaultView.getComputedStyle(arguments[0],null)" + \
        #                ".getPropertyValue('%s')"
        #return self.execute_script(js % (css_property), element)
        return element.value_of_css_property(css_property)
    
    def execute_script(self, script, *args):
        """Executes Javascript code in the browser. Can return an int, bool, string, WebElement, or None"""
        return self.driver.execute_script(script, *args)
           
    def execute_async_script(self, script, *args):
        """Executes Javascript through a callback. Please refer to the Javadoc Selenium documentation."""
        return self.driver.execute_async_script(script, *args)

    def set_async_script_timeout(self, timeout_in_sec):
        """Sets the timeout for execute_async_script, when timeout is reached, exception is raised."""
        self.driver.set_script_timeout(timeout_in_sec)

    # @print_stack_trace
    def wait_for_jquery_ajax_to_complete(self, wait_first=False): # timeout_in_millisec=1000
        """Waits for jQuery AJAX calls to complete via the browser."""
        #script = "var callback = arguments[arguments.length - 1];" \
            # "var checkInactive = function() {{" \
            # "     if ((window.jQuery != null) && (jQuery.active === 0)) return callback();" \
            # "     setTimeout(checkInactive, {0});" \
            # "}};" \
            # "checkInactive();"
        #script = script.format(timeout_in_millisec)
        #self.driver.execute_async_script(script)
        # window.jQuery != null tests if jQuery does exist.
        if wait_first:
            try:
                # print "waiting for the activity"
                # start = time.time()
                self.driver.set_script_timeout(5)
                script = 'var callback = arguments[arguments.length - 1];\n' \
                     'var any_activity_yet = false;\n' \
                     'var checkInactive = function() {\n' \
                     '    var result = (window.jQuery != null) && (jQuery.active === 0);\n' \
                     '    if ((result == true) && (any_activity_yet == true)) {\n' \
                     '        return callback();\n' \
                     '    }\n' \
                     '    if (result == false) {\n' \
                     '        any_activity_yet = true;\n' \
                     '    }\n' \
                     '    setTimeout(checkInactive, 250);\n' \
                     '}\n' \
                     'checkInactive();'
                self.execute_async_script(script)
                # print "time waiting %2.3f seconds" % (time.time() - start)
            except TimeoutException:
                print "async timedout" # 6 seconds is a big enough pause and shouldn't stop test execution
            else:
                print "returning"
                return
        script = "(window.jQuery != null) && (jQuery.active === 0);"
        print 'check for activity'
        self.wait_for_script_expression_to_evaluate_true(script)

    def wait_for_script_expression_to_evaluate_true(self, js, timeout=None):
        """Waits until the given Javascript expression evaluates to true until the timeout."""
        if not timeout:
            timeout = self.timeout
        start = self.now()
        js_is_true = False
        # print 'start waiting'
        while (self.now() - start < timeout):
                js_is_true = self.execute_script("return " + js)
                #print 'Jquery is active: {0}'.format(js_is_true)
                if js_is_true:
                    # print 'ok!'
                    return
                else:
                    # print 'pausing for ajax to complete'
                    self.pause(.25)
        raise TimeoutException("The expression: {0} did not become true after {1} seconds.".format(js, timeout))

    def listener_is_registered_on_element(self, driver, listener_type, element):
        """Expected Condition: listener_type is a string ex: "mouseover", element is a WebElement."""
        registered_listeners = self.driver.execute_script("return jQuery._data(jQuery(arguments[0]).get(0), 'events')",
                                                          element)
        for listener in registered_listeners:
            if listener == listener_type:
                return True
        return False

    def wait_for_listener_to_be_registered_on_element(self, listener_type, element):
        """Wait for an event listener to be registered on a web element that uses jQuery."""
        WebDriverWait(self.driver, self.timeout).until(
                lambda d: self.listener_is_registered_on_element(d, listener_type, element))
 
    def wait_for_alert_to_appear(self):
        """Waits for an alert to appear, returns an Alert object"""
        return WebDriverWait(self.driver, 10).until(alert_is_present())

    def accept_alert_dialog_box(self):
        """Clicks OK/Yes/Accept when a Javascript alert box pops up."""
        self.wait_for_alert_to_appear().accept()
    
    def dismiss_alert_dialog_box(self):
        """Clicks Cancel when a Javascript alert box pops up."""
        self.wait_for_alert_to_appear().dismiss()
        
    @property
    def get_text_from_alert_dialog_box(self):
        """Returns the text in an alert dialog box."""
        return self.wait_for_alert_to_appear().text

    def type_into_alert_dialog_box(self, text):
        """Types into the alert dialog box."""
        self.wait_for_alert_to_appear().send_keys(text)

    def new_select_wrapper(self, locator):
        """Returns a Select helper object to operate on selection elements. Accepts a locator tuple."""
        return Select(self.get_element(locator))

    def new_action_chains(self):
        """Returns an Actions API class that allows Webdriver to control the mouse and keyboard actions as sequence."""
        return ActionChains(self.driver)

    def format_locator(self, locator, string):
        """Formats the locator in a locator tuple"""
        by = locator[0]
        new_locator = locator[1].format(string)
        description = locator[2]
        return by, new_locator, description

    def get_list_of_strings_from_element(self, locator):
        """Returns a list of strings by iterating through a list of elements found by the locator."""
        list_of_strings = []
        for element in self.get_elements(locator):
            list_of_strings.append(element.text)
        return list_of_strings

    def get_list_of_strings_from_elements_attribute(self, locator, attribute):
        """Returns a list of strings that is based on a element's attribute, where the locator represents
        multiple elements."""
        list_of_strings = []
        for element in self.get_elements(locator):
            list_of_strings.append(element.get_attribute(attribute))
        return list_of_strings

    def wait_for_jquery_animation_to_complete(self, selector, wait_to_start=False):
        """Given a locator tuple or jQuery selector string, it will wait for that element to stop animating.
        The element must be controlled by jQuery. Set wait to start if you expect a delay to the animation start"""
        if isinstance(selector, tuple):
            selector = selector[1]
        script = '$("{0}").filter(":animated").length === 0;'.format(selector)
        if wait_to_start:
            script = '$("{0}").filter(":animated").length !== 0;'.format(selector)
            try:
                self.wait_for_script_expression_to_evaluate_true(script, 3)
            except TimeoutException:
                pass
        self.wait_for_script_expression_to_evaluate_true(script)

    def wait_for_element(self, locator, timeout=60, interval=1):
        """Explicitly wait for an element to appear. Polling interval is 1 second"""
        for i in range(timeout):
            try:
                self.driver.find_element(locator[0:2])
                break
            except WebDriverException:
                time.sleep(interval)

    def _text_is_not_empty(self, ignored, element):
        """ExpectedCondition: True if text is not an empty string or an error."""
        try:
            if element.text:
                return True
        except WebDriverException:
            return False

    def wait_for_non_empty_text_to_appear(self, element, timeout=None):
        """Waits for an element to be populated with text."""
        if timeout == None:
            timeout = self.timeout
        if isinstance(element, tuple): # element is a locator tuple
            human_description = element[1]
            element = self.get_element(element)
        WebDriverWait(self.driver, timeout).until((lambda d: self._text_is_not_empty(d, element)),
            "The element has returned blank text or another error occured")

    def _element_is_active(self, driver, attribute, expected_string):
        """Expected Condition: True if attribute matches the expected string.
        This function will switch to the element in focus. Then the element is queried."""
        element = driver.switch_to_active_element()
        if attribute == "tag name":
            return element.tag_name == expected_string
        else:
            return element.get_attribute == expected_string



    def wait_for_active_element(self, attribute, expected_string, timeout=None):
        """Waits for the element to become in focus"""
        if timeout == None:
            timeout = self.timeout
        WebDriverWait(self.driver, timeout).until((lambda d: self._element_is_active(d, attribute, expected_string)),
                                                  "The element did not switch focus to what is expected")
    
    def get_screenshot_as_file(self, file_path):
        """Gets a screenshot from the current browser window and saves it to the path specified."""
        if not self.driver.get_screenshot_as_file(file_path):
            raise Exception("There was an error saving screenshot at: " + file_path)
    
    def set_scope(self, scope):
        """Sets the scope of the browser object to control if the browser session is persistent for the session
         or for the duration of a single test method."""
        self.scope = scope