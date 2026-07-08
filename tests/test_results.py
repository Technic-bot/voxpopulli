from flask import session

def test_open_poll_results(client):
    resp = client.get("/api/polls/123/result")
    jason = resp.json
    assert resp.status_code == 403

def test_open_poll_results(client):
    resp = client.get("/api/polls/789/result")
    jason = resp.json
    assert resp.status_code == 200

def test_unexistent_poll(client):
    resp = client.get("/api/polls/2016/result")
    
    assert resp.status_code == 404
