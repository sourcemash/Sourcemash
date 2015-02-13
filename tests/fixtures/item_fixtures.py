import pytest
from tests.factories import item_factories

@pytest.fixture()
def item(request):
<<<<<<< HEAD
    return item_factories.ItemFactory()
=======
    return item_factories.ItemFactory()

@pytest.fixture()
def ebolaItem(request):
	return item_factories.EbolaItemFactory()

@pytest.fixture()
def oftheItem(request):
	return item_factories.OfTheItemFactory()
>>>>>>> test for empty category, fix import bug
