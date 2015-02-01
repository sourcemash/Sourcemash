from selenium.webdriver.common.by import By
from base import BasePage

class LoginPage(BasePage):
    """Login Page"""

    #base url
    _page_url = "/"

    #locators
    welcome_user = (By.CSS_SELECTOR, ".welcome", "user welcome message")
    
    # Navbar buttons
    register_button = (By.PARTIAL_LINK_TEXT, 'Register', "Register button")
    login_button = (By.PARTIAL_LINK_TEXT, 'Login', "Login button")
    logout_button = (By.PARTIAL_LINK_TEXT, 'Logout', "Logout button")

    #register
    header_text = (By.CSS_SELECTOR, "h1", "page header text")
    email_input_field = (By.CSS_SELECTOR, "input[name='email']", "email input field")
    password_input_field = (By.CSS_SELECTOR, 'input[name="password"]', "password input field")
    confirm_password_input = (By.CSS_SELECTOR, 'input[name="password_confirm"]', "confirm password input")
    submit_button = (By.CSS_SELECTOR, 'button[type="submit"]', "Submit button")
    success_message = (By.CSS_SELECTOR, ".welcome", "user welcome message on register")

    #functions
    def navigate(self):
        self.browser.go_to_relative_url(self._page_url)

    def click_register_button(self):
        self.browser.get_element(self.register_button).click()

    def click_login_button(self):
        self.browser.get_element(self.login_button).click()

    def click_logout_button(self):
        self.browser.get_element(self.logout_button).click()

    # Page Elements
    def get_header_text(self):
        return self.browser.get_element(self.header_text).text

    def type_into_email_field(self, email):
        self.browser.get_element(self.email_input_field).click()
        self.browser.get_element(self.email_input_field).clear()
        self.browser.get_element(self.email_input_field).send_keys(email)

    def type_into_password_field(self, password):
        self.browser.get_element(self.password_input_field).click()
        self.browser.get_element(self.password_input_field).clear()
        self.browser.get_element(self.password_input_field).send_keys(password)

    def type_into_confirm_password_field(self, password):
        self.browser.get_element(self.confirm_password_input).click()
        self.browser.get_element(self.confirm_password_input).clear()
        self.browser.get_element(self.confirm_password_input).send_keys(password)

    def click_submit_button(self):
        self.browser.get_element(self.submit_button).click()

    def get_success_message(self):
        return self.browser.get_element(self.success_message).text

    def get_welcome_user_message(self):
        return self.browser.get_element(self.welcome_user).text