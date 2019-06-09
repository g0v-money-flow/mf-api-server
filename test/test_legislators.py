import os
import re
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
    assert re.match("^/[a-z]+Election/[0-9]{4,4}/regions$", jData['legislator'][0]['link'])

def test_no_target_election_exist(client):
    rv = client.get('/stupidElection/2016/regions')

    assert 404 == rv.status_code

def test_no_target_year_exist(client):
    rv = client.get('/legislatorElection/2011/regions')

    assert 404 == rv.status_code

def test_region_list(client):
    rv = client.get('/legislatorElection/2016/regions')
    jData = json.loads(rv.data)['data']

    assert 200 == rv.status_code
    assert 'regions' in jData
    assert len(jData['regions']) > 1
    assert 'name' in jData['regions'][0]
    assert 'link' in jData['regions'][0]
    assert re.match('^/[a-z]+Election/[0-9]{4,4}/[0-9-]+$', jData['regions'][0]['link'])

