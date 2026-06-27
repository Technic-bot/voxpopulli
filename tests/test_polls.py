from flask import session

def test_latest_poll(client):
    resp = client.get('/api/poll')
    datum = resp.json
    name = datum['name']
    poll_id = datum['id']
    assert name == 'Sunday poll'

def test_poll(client):
    resp = client.get('/api/poll/456')
    datum = resp.json
    name = datum['name']
    options = datum['options']
    assert len(options) == 5
    assert name == '90s poll'

def test_post_ballot(client):
    with client.session_transaction() as session:
        session['voter_id'] = 'Tec'

    resp = client.post(
        '/api/poll/456/ballot',
        json = {
            "ranking": [ 2, 3]
        }
    )

    assert resp.json['ranking'] == 2

def test_malformed_ballot(client):
    with client.session_transaction() as session:
        session['voter_id'] = 'Tec'

    resp = client.post(
        '/api/poll/456/ballot',
        json = {
            "ranking": [2, 45]
        }
    )
        
    assert resp.status_code == 409

def test_get_ballot(client):
    with client.session_transaction() as session:
        session['voter_id'] = 'Jason'

    resp = client.get('/api/poll/456/ballot')
    data = resp.json

    assert len(data['ranking']) == 2

def test_vote_flow(client):
    with client.session_transaction() as session:
        session['voter_id'] = 'Tec'

    resp = client.get('/api/poll/456')
    datum = resp.json
    name = datum['name']
    options = datum['options']
    opt_dic = { o['text'] : o['id'] for o in options}

    exp_opts = { 
        "Kamen rider black transforming": 2,
        "Zelda on a picnic": 3,
        "Cross country roadtrip": 4,
        "Girls in a museum exhibit": 5,
        "CSI cosplay": 6 
    }

    assert opt_dic == exp_opts

    rank_map = { 
        "Girls in a museum exhibit":0,
        "Kamen rider black transforming": 1
    }

    ranking = [
         opt_dic["Girls in a museum exhibit"],
         opt_dic["Kamen rider black transforming"]
    ]
            
    ballot = { 'ranking' : ranking} 
    
    resp = client.post('/api/poll/456/ballot', json = ballot)
    assert resp.status_code == 200

    resp = client.get('/api/poll/456/ballot')
    data = resp.json

    for d in data['ranking']:
        text = d['text']
        assert rank_map[text] == d['ranked'] 

def test_unexistent_poll_cast(client):
    resp = client.post("/api/poll/2016/ballot",
        json = {
            "ranking": [ 2, 3]
        }
    )
    
    assert resp.status_code == 404
