"""
Tests for the /login endpoint
"""

from flask import session

class MockiNaturalistClient():
    """
    Standin for the iNaturalist client from gluon
    """

    def __init__(
        self, email, password, app_id, app_secret,
        api_url, app_url
    ):
        self.email = email
        self.password = password
        self.app_id = app_id
        self.app_secret = app_secret
        self.api_url = api_url
        self.app_url = app_url

        self.input_email = None
        self.input_password = None
        self.input_app_id = None
        self.input_app_secret = None
        self.input_api_url = None
        self.input_app_url = None

    def __call__(
        self, email, password, app_id, app_secret,
        api_url, app_url
    ):
        """
        Called on instantiation of the client
        within the code being tested
        """
        self.input_email = email
        self.input_password = password
        self.input_app_id = app_id
        self.input_app_secret = app_secret
        self.input_api_url = api_url
        self.input_app_url = app_url
        return self

    def _get_new_token(self):
        """
        Called when we check user credentials.
        Checks that our creds are the ones expected.
        """
        try:
            assert self.input_email == self.email
            assert self.input_password == self.password
            assert self.input_app_id == self.app_id
            assert self.input_app_secret == self.app_secret
            assert self.input_api_url == self.api_url
            assert self.input_app_url == self.app_url
        except Exception as exception:
            print(exception)
            raise exception


def test_view(client):
    """
    Tests that we get the right form on a GET
    """
    response = client.get('/login')
    assert response.status_code == 200
    assert (
        b'<input class="input is-large" type="email" name="email" placeholder="Email" autofocus="">'
        in response.data
    )
    assert (
        b'<input class="input is-large" type="password" name="password" placeholder="Password">'
        in response.data
    )

def test_login_succeeds(client, mocker):
    """
    Tests the behavior when a login succeeds
    """
    data = {
        'email': 'dragon@bug.org',
        'password': 'sixlegsisbest'
    }

    mocker.patch(
        'gluon.inaturalist.client.iNaturalistClient',
        MockiNaturalistClient(
            data['email'],
            data['password'],
            'iamanappid',
            'iamanappsecret',
            'https://api.fakeinaturalist.org/v1',
            'https://www.fakeinaturalist.org'
        )
    )

    with client:
        response = client.post('/login', data=data, follow_redirects=True)
        assert response.history[0].status_code == 302
        assert response.status_code == 200
        assert response.request.path == '/'
        assert session['_user_id'] == ' '.join([data['email'], data['password']])

def test_login_fails(client, mocker):
    """
    Tests the behavior when a login fails
    """
    data = {
        'email': 'dragon@bug.org',
        'password': 'sixlegsisbest'
    }

    mocker.patch(
        'gluon.inaturalist.client.iNaturalistClient',
        MockiNaturalistClient(
            data['email'],
            'twolegsarebest',
            'iamanappid',
            'iamanappsecret',
            'https://api.fakeinaturalist.org/v1',
            'https://www.fakeinaturalist.org'
        )
    )

    with client:
        response = client.post('/login', data=data, follow_redirects=True)
        assert response.history[0].status_code == 302
        assert response.status_code == 200
        assert response.request.path == '/login'
        assert '_user_id' not in session

def test_login_follows_redirect(client, mocker):
    """
    Tests that a successfull login redirects back to the
    page that created the login request
    """
    data = {
        'email': 'dragon@bug.org',
        'password': 'sixlegsisbest'
    }

    mocker.patch(
        'gluon.inaturalist.client.iNaturalistClient',
        MockiNaturalistClient(
            data['email'],
            data['password'],
            'iamanappid',
            'iamanappsecret',
            'https://api.fakeinaturalist.org/v1',
            'https://www.fakeinaturalist.org'
        )
    )

    response = client.post(
        '/login', data=data, query_string={'next': '/notapage'},
        follow_redirects=True
    )
    assert response.history[0].status_code == 302
    assert response.status_code == 404
    assert response.request.path == '/notapage'
