import pytest
from tests.factories import item_factories

@pytest.yield_fixture(scope='function')
def item(request):
    yield item_factories.ItemFactory()