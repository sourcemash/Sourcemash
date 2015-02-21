import pytest
from tests.pages.login import LoginPage
from tests.pages.dashboard import DashboardPage

class TestLogin:

    def test_logout(self, driver, logged_in_user):
        page = LoginPage(driver)
        page.click_logout_button();

        assert "Login" in page.get_header_text()

    def test_register(self, driver):
        page = LoginPage(driver)
        page.navigate()

        page.click_register_button()
        page.type_into_email_field("GenericEmail@gmail.com")
        page.type_into_password_field("password")
        page.type_into_confirm_password_field("password")
        page.click_submit_button()

        assert "GenericEmail@gmail.com" in page.get_success_message()

class TestFeeds:

    def test_feeds_list(self, db, driver, logged_in_user, feed):
        logged_in_user.subscribed.append(feed)
        db.session.commit()

        page = DashboardPage(driver)
        page.navigate()
        assert feed.title in page.get_feeds_list_text()

    def test_add_valid_url(self, db, driver, logged_in_user, real_feed):
        page = DashboardPage(driver)
        page.navigate()

        page.type_into_url_field(real_feed.url)
        page.click_submit_button()

        assert real_feed.title in page.get_feeds_list_text(wait_first=True)

    def test_add_invalid_url(self, db, driver, logged_in_user, feed):
        page = DashboardPage(driver)
        page.navigate()

        page.type_into_url_field(feed.url)
        page.click_submit_button()

        assert feed.title not in page.get_feeds_list_text()
        assert "not a valid feed" in page.get_url_input_errors_text()