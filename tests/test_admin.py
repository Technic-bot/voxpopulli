
def test_post_poll(client):
    resp = client.post('/admin/poll', json={
            'name': 'Sunday Poll',
            'duration': 1,
            'suggestions': [
                "Leviathan with a tophat",
                "A dog playing risk",
                "A rancher ranchin"
            ]
           })
    new_poll_id = resp.json['id']
    suggestions = resp.json['suggestions']

    assert suggestions == 3

def test_upload_flow(client):
    opts = ['The party playing DnD',
            'Marketable plushie version or protagonist',
            'Side character building model kits']
    name = 'Faux poll'
    poll = {
        'name' : name,
        'duration': 1,
        'suggestions': opts
    }
    resp = client.post("/admin/poll", 
        json = poll
    )
    
    poll_id = resp.json['id']
    resp = client.get(f"/poll/{poll_id}")
    poll = resp.json
    resp_options = poll['options']

    assert poll['name'] == name
    for opt in resp_options:
        assert opt['text'] in opts



