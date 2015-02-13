import pytest
from tests.factories import item_factories

@pytest.fixture()
def item(request):
    return item_factories.ItemFactory()

@pytest.fixture()
def ebolaItem(request):
	return item_factories.EbolaItemFactory()

@pytest.fixture()
def oftheItem(request):
	return item_factories.OfTheItemFactory()