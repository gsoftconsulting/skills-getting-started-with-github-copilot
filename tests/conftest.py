import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

# Snapshot of the initial activities state taken at import time, before any
# test can mutate the module-level dict.
_INITIAL_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app, raise_server_exceptions=True)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore the in-memory store to its original state before every test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_INITIAL_ACTIVITIES))
    yield
