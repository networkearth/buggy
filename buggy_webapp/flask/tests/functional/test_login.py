def test_view(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'<input class="input is-large" type="email" name="email" placeholder="Email" autofocus="">' in response.data
    assert b'<input class="input is-large" type="password" name="password" placeholder="Password">' in response.data
