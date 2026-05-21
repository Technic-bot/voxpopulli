
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
