from flask import session

def test_view(client):
    with client.session_transaction() as session:
        session['_user_id'] = 'dragon@bug.org sixlegsisbest'
    
    response = client.get('/logout')
    
    assert response.status_code == 200
    assert '<button class="button is-block is-info is-large is-fullwidth">Logout</button>' in response.data.decode('utf-8')

def test_post(client):
    with client:
        with client.session_transaction() as sesh:
            sesh['_user_id'] = 'dragon@bug.org sixlegsisbest'
        
        response = client.post('/logout', follow_redirects=True)
        
        assert '_user_id' not in session
        assert response.history[0].status_code == 302
        assert response.status_code == 200
        assert response.request.path == '/'