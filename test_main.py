from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# test keys for /data/ship 

def test_read_ship():
    response = client.get("/data/ship")
    assert response.status_code == 200
    assert list(response.json()[0].keys()) == [
    "ship_id",
    "name",
    "code"
    ]

# test keys for /data/embark

def test_read_embark():
    response = client.get("/data/embark")
    assert response.status_code == 200
    assert list(response.json()[0].keys()) == [
    'voyage_id', 
    'added_date', 
    'oci_completed_core', 
    'moci_completed_core', 
    'checkedin_couch', 
    'onboard_couch', 
    'expected_couch', 
    'code', 
    'number'
    ]

# test keys for /data/overview

def test_read_overview():
    response = client.get("/data/overview")
    assert response.status_code == 200
    assert list(response.json()[0].keys()) == [
    'voyage_id', 
    'added_date', 
    'oci_completed_core', 
    'moci_completed_core', 
    'checkedin_couch', 
    'onboard_couch', 
    'expected_couch', 
    'code', 
    'number', 
    'end_date', 
    'start_date'
    ]

# test keys for /data/voyage

def test_read_environment():
    response = client.get("/data/voyage")
    assert response.status_code == 200
    assert list(response.json().keys()) == [
    'DF', 
    'DM', 
    'DW', 
    'DD', 
    'WW'
    ]

# test keys for /data/avg/voyage

def test_read_avg_voyage():
    response = client.get("/data/avg/voyage")
    assert response.status_code == 200
    assert list(response.json()[0].keys()) == [
    'voyage_id', 
    'checkedin_time', 
    'onboard_time', 
    'actual_count', 
    'onboard_couch', 
    'checkedin_couch', 
    'avg_checkedin_couch', 
    'avg_onboard_couch', 
    'ship'
    ]

# test /model/table for title

def test_read_table():
    response = client.get("/model/table")
    assert response.status_code == 200
    responseList = []
    for eachDict in response.json():
        response1 = eachDict['title']
        responseList.append(response1)
    assert responseList == [
    'Ship Name', 
    'Ship Number', 
    'Embarkation Count', 
    'OCI Count', 
    'MOCI Count', 
    'CheckIn Time', 
    'OnBoard Time'
    ]

# test keys for /data/voyage

def test_read_voyage():
    response = client.get("/data/voyage")
    assert response.status_code == 200
    assert list(response.json()['DF'][0].keys()) == [
    'voyage_id', 
    'checkedin_time', 
    'onboard_time', 
    'actual_count', 
    'onboard_couch', 
    'checkedin_couch'
    
    ]
