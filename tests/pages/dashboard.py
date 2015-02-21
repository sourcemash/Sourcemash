from selenium.webdriver.common.by import By
from base import BasePage

class DashboardPage(BasePage):
    """Dashboard Page"""

    #base url
    _page_url = "/dashboard"

    #locators
    header_text = (By.CSS_SELECTOR, "h1", "page header text")
    dashboard_button = (By.PARTIAL_LINK_TEXT, "Dashboard", "dashboard button")
    feeds_list = (By.CSS_SELECTOR, ".feeds", "feeds list")

    url_input_field = (By.CSS_SELECTOR, "#url", "url input field")
    url_input_errors = (By.CSS_SELECTOR, ".url-errors", "url input errors")
    submit_button = (By.CSS_SELECTOR, 'button[type="submit"]', "Submit button")

    #functions
    def navigate(self):
        self.browser.go_to_relative_url(self._page_url)

    def click_dashboard_button(self):
        self.browser.get_element(self.dashboard_button).click()

    # Page Elements
    def get_header_text(self):
        return self.browser.get_element(self.header_text).text

    def get_feeds_list_text(self, wait_first=False, interval=0.5):
        if wait_first:
            interval = 5

        return self.browser.get_element(self.feeds_list, wait_first=wait_first, interval=interval).text

    def get_url_input_errors_text(self):
        return self.browser.get_element(self.url_input_errors).text

    def type_into_url_field(self, url):
        self.browser.get_element(self.url_input_field).click()
        self.browser.get_element(self.url_input_field).clear()
        self.browser.get_element(self.url_input_field).send_keys(url)

    def click_submit_button(self):
        self.browser.get_element(self.submit_button).click()
