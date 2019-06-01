import os
import tempfile
import json
import pytest
from app import app


@pytest.fixture
def client():
    client = app.test_client()
    yield client

def test_election_list(client):
    rv = client.get('/elections')
    jData = json.loads(rv.data)

    assert 200 == rv.status_code
    assert "hello" in jData
    assert "world" == jData['hello']
