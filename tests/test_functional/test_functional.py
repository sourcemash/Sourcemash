import pytest
from tests.pages.login import LoginPage
from tests.pages.feeds import FeedsPage

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

        page = FeedsPage(driver)
        page.navigate()
        assert feed.title in page.get_feeds_list_text()