"""
Tests for the /submissions endpoint
"""

import re
import json
import httpretty


@httpretty.activate
def test_view_w_login(client):
    """
    Tests that submissions works as expected when someone is logged in
    """
    with client.session_transaction() as session:
        session['_user_id'] = 'dragon@bug.org sixlegsisbest'

    httpretty.register_uri(
        httpretty.GET, 'http://localhost:5002/submissions',
        body=json.dumps([
            {
                'instance': 12, 'images': [1, 2]
            },
            {
                'instance': 32, 'images': [4, 20]
            }
        ])
    )

    response = client.get('/submissions')

    assert json.loads(httpretty.last_request().body.decode('utf-8')) == {
        'email': 'dragon@bug.org', 'kobo_password': 'chitinisking',
        'kobo_username': 'beetlebub', 'kobo_uid': 'iguessiamauid'
    }
    assert response.status_code == 200
    assert (
        '<img src="/image/12/1" class="rounded float-left" style="height: 100px">'
        in response.data.decode('utf-8')
    )
    assert (
        '<img src="/image/12/2" class="rounded float-left" style="height: 100px">'
        not in response.data.decode('utf-8')
    )
    assert (
        '<img src="/image/32/4" class="rounded float-left" style="height: 100px">'
        in response.data.decode('utf-8')
    )
    assert (
        '<img src="/image/32/20" class="rounded float-left" style="height: 100px">'
        not in response.data.decode('utf-8')
    )

    assert (
        re.search(
            r'<label class="form-check-label" for="flexCheckChecked">\s*12\s*<\/label>',
            response.data.decode('utf-8')
        )
        is not None
    )
    assert (
        re.search(
            r'<label class="form-check-label" for="flexCheckChecked">\s*32\s*<\/label>',
            response.data.decode('utf-8')
        )
        is not None
    )

def test_view_wo_login(client):
    """
    Tests that submissions redirects to login when no one is logged in
    """
    response = client.get('/submissions', follow_redirects=True)
    assert response.history[0].status_code == 302
    assert response.status_code == 200
    assert response.request.path == '/login'
    assert response.request.query_string.decode('utf-8') == 'next=%2Fsubmissions'

def test_view_wo_api(client):
    """
    Tests that submissions returns a 500 when the api is unreachable
    """
    with client.session_transaction() as session:
        session['_user_id'] = 'dragon@bug.org sixlegsisbest'

    response = client.get('/submissions')
    assert response.status_code == 500

@httpretty.activate
def test_post(client):
    """
    Tests that a POST submits a job as expected
    """
    with client.session_transaction() as session:
        session['_user_id'] = 'dragon@bug.org sixlegsisbest'

    httpretty.register_uri(
        httpretty.POST, 'http://localhost:5002/job',
        body=json.dumps([])
    )

    # for when we redirect
    httpretty.register_uri(
        httpretty.GET, 'http://localhost:5002/submissions',
        body=json.dumps([
            {
                'instance': 12, 'images': [1, 2]
            },
            {
                'instance': 32, 'images': [4, 20]
            }
        ])
    )

    data = {
        12: 'checked',
        32: 'checked'
    }

    response = client.post('/submissions', data=data, follow_redirects=True)
    assert response.history[0].status_code == 302
    assert response.status_code == 200
    assert response.request.path == '/submissions'
    assert json.loads(httpretty.latest_requests()[0].body.decode('utf-8')) == {
        'kobo_username': 'beetlebub', 'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid', 'inaturalist_email': 'dragon@bug.org',
        'inaturalist_password': 'sixlegsisbest', 'client_id': 'iamanappid',
        'client_secret': 'iamanappsecret', 'instances': '12,32'
    }

def test_post_wo_api(client):
    """
    Tests that a POST returns 500 when the api is unreachable
    """
    with client.session_transaction() as session:
        session['_user_id'] = 'dragon@bug.org sixlegsisbest'

    data = {
        12: 'checked',
        32: 'checked'
    }

    response = client.post('/submissions', data=data, follow_redirects=True)
    assert response.status_code == 500
