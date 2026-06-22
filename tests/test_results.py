from flask import session

def test_poll_results(client):
    resp = client.get("/api/poll/789/result")
    jason = resp.json
    print(jason)
    return
