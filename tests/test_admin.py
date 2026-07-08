from datetime import datetime, timedelta

def test_post_poll(client):
    now = datetime.now()
    closing = now + timedelta(hours=1)
    closes_at = closing.strftime("%Y-%m-%d %H:%M:%S")
    resp = client.post('/api/admin/poll', json={
            'name': 'Sunday Poll',
            'closes_at': closes_at,
            'suggestions': [
                "Leviathan with a tophat",
                "A dog playing risk",
                "A rancher ranchin"
            ]
           })
    new_poll_id = resp.json['id']
    suggestions = resp.json['suggestions']

    assert suggestions == 3

def test_empty_suggestion(client):
    now = datetime.now()
    closing = now + timedelta(hours=1)
    closes_at = closing.strftime("%Y-%m-%d %H:%M:%S")
    resp = client.post('/api/admin/poll', json={
            'name': 'Empty Poll',
            'closes_at': closes_at,
            'suggestions': [
                "A non empy suggestion",
                " ",
            ]
           })
    new_poll_id = resp.json['id']
    suggestions = resp.json['suggestions']

    assert suggestions == 1

def test_upload_flow(client):
    now = datetime.now()
    closing = now + timedelta(hours=1)
    closes_at = closing.strftime("%Y-%m-%d %H:%M:%S")
    opts = ['The party playing DnD',
            'Marketable plushie version or protagonist',
            'Side character building model kits']
    name = 'Faux poll'
    poll = {
        'name' : name,
        'closes_at': closes_at,
        'suggestions': opts
    }
    resp = client.post("/api/admin/poll", 
        json = poll
    )
    
    poll_id = resp.json['id']
    resp = client.get(f"/api/polls/{poll_id}")
    poll = resp.json
    resp_options = poll['options']

    assert poll['name'] == name
    for opt in resp_options:
        assert opt['text'] in opts



