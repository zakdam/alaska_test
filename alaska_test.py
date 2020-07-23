import requests
import json

test_bears = [{"bear_id":None, "bear_type":"POLAR","bear_name":"POLAR_TEST_BEAR","bear_age":1.0},
              {"bear_id":None, "bear_type":"BROWN","bear_name":"BROWN_TEST_BEAR","bear_age":2.0},
              {"bear_id":None, "bear_type":"BLACK","bear_name":"BLACK_TEST_BEAR","bear_age":3.0},
              {"bear_id":None, "bear_type":"GUMMY","bear_name":"GUMMY_TEST_BEAR","bear_age":4.0}]

bear_types = ["POLAR", "BROWN", "BLACK", "GUMMY"]

def test_initial_delete():
    r = requests.delete("http://localhost:8091/bear")
    assert r.status_code == 200
    r = requests.get("http://localhost:8091/bear")
    assert r.status_code == 200
    assert r.text == "[]"

# check if info is available
def test_info():
    r = requests.get("http://localhost:8091/info")
    assert r.status_code == 200

# create all possible bear types; save their ids for later usage
def test_create():
    for bear in test_bears:
        bear_no_id = {k: v for k, v in bear.items() if k not in {'bear_id'}}
        r = requests.post("http://localhost:8091/bear", data = json.dumps(bear_no_id))
        assert r.status_code == 200
        bear["bear_id"] = int(r.text)

# read all bears; check if bear is in test_bears
def test_read_all():
    r = requests.get("http://localhost:8091/bear")
    assert r.status_code == 200
    for bear in r.json():
        assert bear in test_bears

# read all bears by id; compare received values with expected values
def test_read():
    for bear in test_bears:
        r = requests.get("http://localhost:8091/bear/" + str(bear["bear_id"]))
        assert r.status_code == 200
        assert r.json() == bear

# update bear type, name and age; read back; compare received values with expected values
def test_update_age():
    for bear in test_bears:
        bear["bear_type"] = next(x for x in bear_types if x != bear["bear_type"])
        bear["bear_name"] = "upd_" + bear["bear_name"] + "_upd"
        bear["bear_age"] = bear["bear_age"] + 1.0
        bear_no_id = {k: v for k, v in bear.items() if k not in {'bear_id'}}
        r = requests.put("http://localhost:8091/bear/" + str(bear["bear_id"]), data = json.dumps(bear_no_id))
        assert r.status_code == 200, json.dumps(bear)
        r = requests.get("http://localhost:8091/bear/" + str(bear["bear_id"]))
        assert r.status_code == 200
        assert r.json() == bear

# delete bears by id; read back; check if empty
def test_delete():
    for bear in test_bears:
        r = requests.delete("http://localhost:8091/bear/" + str(bear["bear_id"]))
        assert r.status_code == 200
        r = requests.get("http://localhost:8091/bear/" + str(bear["bear_id"]))
        assert r.status_code == 200
        assert r.text == "EMPTY"

# create test entries; delete them all; read back; check if empty
def test_delete_all():
    for bear in test_bears:
        bear_no_id = {k: v for k, v in bear.items() if k not in {'bear_id'}}
        r = requests.post("http://localhost:8091/bear", data = json.dumps(bear_no_id))
        assert r.status_code == 200
    r = requests.delete("http://localhost:8091/bear")
    assert r.status_code == 200
    r = requests.get("http://localhost:8091/bear")
    assert r.status_code == 200
    assert r.text == "[]"
