import pytest
from tests.factories import user_item_factories

@pytest.fixture()
def user_item(request):
    return user_item_factories.UserItemFactory()


@pytest.fixture()
def user_item_upvote(request):
    return user_item_factories.UserItemUpvoteFactory()


@pytest.fixture()
def user_item_downvote(request):
    return user_item_factories.UserItemDownvoteFactory()