import pytest
from tests.factories import user_factories, role_factories, feed_factories
from tests.pages.login import LoginPage
from app.models import User

@pytest.fixture()
def user(request):
    return user_factories.UserFactory(subscribed=[])

@pytest.fixture()
def userWithFeed(request):
    feed = feed_factories.FeedFactory()
    return user_factories.UserFactory(subscribed=[feed])

@pytest.fixture()
def logged_in_user(db, driver):
    user = User(email="test@gmail.com", password="pass", active=True)
    db.session.add(user)
    db.session.commit()

    page = LoginPage(driver)
    page.navigate()

    page.click_login_button()

    assert "Login" in page.get_header_text()

    page.type_into_email_field(user.email)
    page.type_into_password_field(user.password)
    page.click_submit_button()

    assert "Hello" in page.get_welcome_user_message()

    return user