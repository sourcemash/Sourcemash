import pytest
from worker.categorize import Categorizer

@pytest.fixture()
def categorizer(request):
    return Categorizer()
