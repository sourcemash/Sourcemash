import pytest

class TestLogin:


    def test_login(self, browser, logged_in_user):
        welcome = browser.find_element_by_css_selector('.welcome').text
        assert logged_in_user.email in welcome

    def test_logout(self, browser, logged_in_user):
        browser.find_element_by_link_text('Logout').click();

        assert "login" in browser.current_url

    def test_register(self, browser):
        browser.get("http://localhost:5000/register")

        # enter email
        email = browser.find_element_by_css_selector('input[name="email"]')
        email.send_keys("GenericEmail@gmail.com")

        # enter password
        password = browser.find_element_by_css_selector('input[name="password"]')
        password.send_keys("password")

        # enter password_confirm
        password_confirm = browser.find_element_by_css_selector('input[name="password_confirm"]')
        password_confirm.send_keys("password")

        # click submit
        button = browser.find_element_by_css_selector('button[type="submit"]')
        button.click()

        welcome = browser.find_element_by_css_selector('.welcome').text
        assert "GenericEmail@gmail.com" in welcome
