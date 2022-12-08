"""
Tests for the /image endpoint
"""

import json
import httpretty

@httpretty.activate
def test_w_login(client):
    """
    Tests endpoint works properly when someone is logged in
    """
    with client.session_transaction() as sesh:
        sesh['_user_id'] = 'dragon@bug.org sixlegsisbest'

    httpretty.register_uri(
        httpretty.GET, 'http://localhost:5002/image',
        body=b'flowerpower'
    )

    response = client.get('/image/32/4')
    assert response.data == b'flowerpower'
    assert response.status_code == 200
    assert response.headers[0] == ('Content-Type', 'image/jpeg')
    assert response.headers[2] == ('Cache-Control', 'private, max-age=7200')
    assert json.loads(httpretty.last_request().body.decode('utf-8')) == {
        'kobo_username': 'beetlebub', 'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid', 'instance': 32, 'id': 4
    }

def test_wo_login(client):
    """
    Tests endpoint redirects when someone is not logged in
    """
    response = client.get('/image/32/4', follow_redirects=True)
    assert response.history[0].status_code == 302
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert response.request.query_string.decode('utf-8') == 'next=%2Fimage%2F32%2F4'

def test_wo_api(client):
    """
    Tests we get a 500 when api is not reachable
    """
    with client.session_transaction() as sesh:
        sesh['_user_id'] = 'dragon@bug.org sixlegsisbest'

    response = client.get('/image/32/4')
    assert response.status_code == 500
    