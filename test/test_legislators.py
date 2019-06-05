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
    jData = json.loads(rv.data)['data']

    assert 200 == rv.status_code
    assert 'legislator' in jData
    assert 2 == len(jData['legislator'])
    assert 'year' in jData['legislator'][0]
    assert 'link' in jData['legislator'][0]

