import pytest
from tests.factories import user_category_factories

@pytest.fixture()
def user_category(request):
    return user_category_factories.UserCategoryFactory()
