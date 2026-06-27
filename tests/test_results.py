from flask import session

def test_poll_results(client):
    resp = client.get("/api/poll/789/result")
    jason = resp.json
    return

def test_unexistent_poll(client):
    resp = client.get("/api/poll/2016/result")
    
    assert resp.status_code == 404
