import pytest

class TestLogin:

    def test_login(self, driver, logged_in_user):
        welcome = driver.find_element_by_css_selector('.welcome').text
        assert logged_in_user.email in welcome

    def test_logout(self, driver, logged_in_user):
        driver.find_element_by_link_text('Logout').click();

        assert "login" in driver.current_url

    def test_register(self, driver):
        driver.get("http://localhost:5000/register")

        # enter email
        email = driver.find_element_by_css_selector('input[name="email"]')
        email.send_keys("GenericEmail@gmail.com")

        # enter password
        password = driver.find_element_by_css_selector('input[name="password"]')
        password.send_keys("password")

        # enter password_confirm
        password_confirm = driver.find_element_by_css_selector('input[name="password_confirm"]')
        password_confirm.send_keys("password")

        # click submit
        button = driver.find_element_by_css_selector('button[type="submit"]')
        button.click()

        welcome = driver.find_element_by_css_selector('.welcome').text
        assert "GenericEmail@gmail.com" in welcome

class TestFeeds:

    def test_feeds_list(self, db, driver, logged_in_user, feed):
        logged_in_user.subscribed.append(feed)
        db.session.commit()

        driver.find_element_by_link_text('Feeds').click();

        feeds_list = driver.find_element_by_css_selector('.feeds').text
        assert feed.title in feeds_list