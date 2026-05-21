from flask import session

def test_latest_poll(client):
    resp = client.get('/poll')
    datum = resp.json
    name = datum['name']
    poll_id = datum['id']
    assert name == 'Sunday poll'

def test_poll(client):
    resp = client.get('/poll/456')
    datum = resp.json
    name = datum['name']
    options = datum['options']
    assert len(options) == 2
    assert name == '90s poll'

def test_ballot(client):
    with client.session_transaction() as session:
        session['voter_id'] = 'Tec'

    resp = client.post(
        '/poll/456/ballot',
        json = {
        "rankings": [
                {'rank': 1, 'id': 2},
                {'rank': 2, 'id': 3},
            ]
        }
    )

    assert resp.json['rankings'] == 2

def test_malformed_ballot(client):
    with client.session_transaction() as session:
        session['voter_id'] = 'Tec'

    resp = client.post(
        '/poll/456/ballot',
        json = {
        "rankings": [
                {'rank': 1, 'id': 2},
                # Suggestion 45 does not exist
                {'rank': 2, 'id': 45},
            ]
        }
    )
        
    assert resp.status_code == 409

