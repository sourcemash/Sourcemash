import pytest
from tests.factories import user_factories, role_factories, feed_factories, item_factories
from tests.pages.login import LoginPage
from sourcemash.models import User

@pytest.fixture()
def user(request):
    return user_factories.UserFactory(subscribed=[])

@pytest.fixture()
def userWithFeed(request):
    feed = feed_factories.FeedFactory()
    return user_factories.UserFactory(subscribed=[feed])

@pytest.fixture()
def userWithPopulatedFeed(request):
    feed = feed_factories.FeedFactory(items=[item_factories.ItemFactory(categories=["News", "Technology"]) for i in range(5)])
    return user_factories.UserFactory(subscribed=[feed])

@pytest.fixture()
def userWithPopulatedFeedAndNoSuggestedContent(request):
    feed = feed_factories.FeedFactory(items=[item_factories.ItemFactory(categories=["News", "Technology"]) for i in range(5)])
    return user_factories.UserFactory(subscribed=[feed], show_suggested_content=False)

@pytest.fixture()
def userWithRealFeed(request):
    feed = feed_factories.TechCrunchFeedFactory()
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

    assert "dashboard" in page.browser.get_current_url

    return user
