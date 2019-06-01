import os
import tempfile
import json
import pytest
from app import app


@pytest.fixture
def client():
    # turns all warnings into errors for this module

    client = app.test_client()
    yield client

def test_election_list(client):
    rv = client.get('/elections')
    jData = json.loads(rv.data)

    assert "hello" in jData
    assert "world" == jData['hello']
