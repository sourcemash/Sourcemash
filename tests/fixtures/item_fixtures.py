import pytest
from tests.factories import item_factories

@pytest.fixture()
def item(request):
    return item_factories.ItemFactory()


@pytest.fixture()
def ebolaItem(request):
	return item_factories.EbolaItemFactory()


@pytest.fixture()
def itemWithCategory(request):
	return item_factories.ItemFactory(categories=["News", "Technology"])


@pytest.fixture()
def itemsWithCategory(request):
	return [item_factories.ItemFactory(categories=["News", "Technology"]) for i in range(5)]
