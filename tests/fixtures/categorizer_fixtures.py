import pytest
from worker_tasks.categorize import Categorizer

@pytest.fixture()
def categorizer(request):
    return Categorizer()
