
def test_latest_poll(client):
    resp = client.get('/poll')
    assert resp.data == b'Mario Jumping over a koopa'

def test_poll(client):
    resp = client.get('/poll/456')
    assert resp.data == b'Geats transforming'
