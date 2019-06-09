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
    assert re.match('^/[a-z]+Election/[0-9]{4,4}/constitutions/[0-9-]+$', jData['regions'][0]['link'])
    
def test_show_wrong_type_constitution(client):
    rv = client.get('/legisrElection/2016/constitutions/63')

    assert 404 == rv.status_code

def test_show_nodata_year_constitution(client):
    rv = client.get('/legislatorElection/2011/constitutions/63')

    assert 404 == rv.status_code

def test_show_nonexist_constitution(client):
    rv = client.get('/legislatorElection/2016/constitutions/63')

    assert 404 == rv.status_code

def test_show_a_constitution(client):
    rv = client.get('/legislatorElection/2016/constitutions/63-000-01-000-0000')
    jData = json.loads(rv.data)['data']

    assert 200 == rv.status_code
    assert 'id' in jData
    assert '63-000-01-000-0000' == jData['id']
    assert 'name' in jData
    assert 'candidates' in jData
    assert len(jData['candidates']) > 1
    assert 'name' in jData['candidates'][0]
    assert 'id' in jData['candidates'][0]
    assert 'party' in jData['candidates'][0]
    assert 'is_elected' in jData['candidates'][0]
    assert 'num_of_vote' in jData['candidates'][0]
    assert 'rate_of_vote' in jData['candidates'][0]
    assert 'finance_data' in jData['candidates'][0]
    assert 'detail' in jData['candidates'][0]
    assert re.match('^/[a-z]+Election/[0-9]{4,4}/candidates/[0-9]+$', jData['candidates'][0]['detail'])

    assert 'constitutions' in jData
    assert len(jData['constitutions']) > 1
    assert 'name' in jData['constitutions'][0]
    assert 'link' in jData['constitutions'][0]
    assert re.match('^/[a-z]+Election/[0-9]{4,4}/constitutions/[0-9-]+$', jData['constitutions'][0]['link'])
    for c in jData['constitutions']:
        assert jData['id'] != c['link'].split('/')[-1]
    
def test_show_wrong_type_candidate(client):
    rv = client.get('/legisrElection/2016/candidates/63')

    assert 404 == rv.status_code

def test_show_nodata_year_candidate(client):
    rv = client.get('/legislatorElection/2011/candidates/63')

    assert 404 == rv.status_code

def test_show_nonexist_constitution(client):
    rv = client.get('/legislatorElection/2016/candidates/111163')

    assert 404 == rv.status_code

def test_show_a_candidate(client):
    rv = client.get('/legislatorElection/2016/candidates/2')
    jData = json.loads(rv.data)['data']

    assert 200 == rv.status_code
    assert 'name' in jData
    assert 'id' in jData
    assert 'party' in jData
    assert 'is_elected' in jData
    assert 'num_of_vote' in jData
    assert 'rate_of_vote' in jData
    assert 'finance_data' in jData
    assert 'income' in jData['finance_data']
    assert 'outcome' in jData['finance_data']

