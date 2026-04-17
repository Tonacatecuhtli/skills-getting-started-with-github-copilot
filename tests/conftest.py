import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient and restore the in-memory `activities` after each test.

    This keeps tests isolated (Arrange-Act-Assert) so one test's changes
    don't affect others.
    """
    original = copy.deepcopy(activities)
    with TestClient(app) as c:
        yield c

    # Restore global state
    activities.clear()
    activities.update(original)
